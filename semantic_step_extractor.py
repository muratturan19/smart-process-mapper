import argparse
import json
import logging
import os
import re
import spacy
import warnings
from typing import Optional

try:
    from transformers import (
        AutoTokenizer,
        AutoModelForCausalLM,
        pipeline,
    )
except Exception as exc:  # pragma: no cover - transformers is optional
    AutoTokenizer = None
    AutoModelForCausalLM = None
    pipeline = None
    warnings.warn(
        "transformers not available (%s). Install the 'transformers' and "
        "'huggingface_hub' packages manually to enable LLM features." % exc
    )

try:
    from huggingface_hub import snapshot_download
except Exception as exc:
    snapshot_download = None
    warnings.warn(
        "huggingface_hub not available (%s). Install the package manually "
        "to enable LLM features." % exc
    )

try:
    nlp = spacy.load("tr_core_news_md")
except OSError:
    warnings.warn(
        "spaCy model 'tr_core_news_md' is not installed. "
        "Install it with "
        "`pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl` "
        "and rerun. Falling back to a blank Turkish pipeline."
    )
    nlp = spacy.blank("tr")
    if "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")

# Optional LLM pipeline
llm_pipeline: Optional["pipeline"] = None


def ensure_llm_pipeline() -> Optional["pipeline"]:
    """Initialize the Kocdigital LLM pipeline if possible.

    If the ``HF_HOME`` environment variable is set, ``snapshot_download`` will
    operate in ``local_files_only`` mode to avoid network access.
    """
    global llm_pipeline
    if llm_pipeline is not None:
        return llm_pipeline

    if not (AutoTokenizer and AutoModelForCausalLM and pipeline):
        logging.warning("transformers library is not available; LLM disabled")
        return None

    if snapshot_download is None:
        logging.warning("huggingface_hub is not available; LLM disabled")
        return None

    model_id = "KOCDIGITAL/Kocdigital-LLM-8b-v0.1"
    try:
        local_only = bool(os.environ.get("HF_HOME"))
        model_dir = snapshot_download(
            repo_id=model_id,
            local_files_only=local_only,
            resume_download=True,
            quiet=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(model_dir, local_files_only=True)
        llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    except Exception as exc:  # pragma: no cover - model download may fail
        llm_pipeline = None
        logging.error("Kocdigital LLM could not be loaded: %s", exc)
    return llm_pipeline

def regex_based_extract_steps(text: str) -> list[str]:
    """Return a list of ordered steps for numbered instructions."""
    pattern = re.compile(r"^\s*\d+[\.)]\s*(.*)")
    steps: list[str] = []
    current: list[str] = []

    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            if current:
                steps.append(" ".join(current).strip())
                current = []
            step = match.group(1).strip()
            if step:
                current.append(step)
        elif current:
            stripped = line.strip()
            if stripped:
                current.append(stripped)

    if current:
        steps.append(" ".join(current).strip())

    return steps


def semantic_extract_steps(text: str) -> list[str]:
    """Extract action phrases from free-form Turkish text using spaCy."""
    doc = nlp(text)
    steps: list[str] = []
    seen: set[str] = set()

    for sent in doc.sents:
        for token in sent:
            if token.pos_ != "VERB" or token.dep_ not in {"ROOT", "conj"}:
                continue

            obj_token = None
            for child in token.children:
                if child.dep_ in {"obj", "obl"} and child.pos_ in {"NOUN", "PROPN"}:
                    obj_token = child
                    break

            verb = token.lemma_
            if verb.endswith("mek") or verb.endswith("mak"):
                verb = verb[:-3]

            phrase = f"{obj_token.lemma_ + ' ' if obj_token else ''}{verb}".strip()
            if phrase and phrase not in seen:
                seen.add(phrase)
                steps.append(phrase)

    return steps


def llm_extract_steps(text: str) -> list[str]:
    """Use the optional LLM to generate numbered steps from text."""
    if ensure_llm_pipeline() is None:
        raise RuntimeError("LLM pipeline is not available")

    prompt = f"""Sen bir Türkçe konuşan süreç analistisin.
    Görevin, verilen metinlerdeki anlatımları dikkatle inceleyip, bunlardan sade, mantıksal ve sıralı işlem adımları oluşturmaktır.

    Her bir adım:
    - Kısa ve öz olmalı (maks. 15 kelime)
    - Fiille başlamalı
    - Gereksiz bağlaç veya detay içermemeli
    - Gramer açısından doğru olmalı

    Aşağıdaki metni işle ve sadece numaralı işlem adımlarını listele.

    {text}

    Çıktı formatı:
    1. ...
    2. ...
    3. ...

    Adımlar:
    """
    output = llm_pipeline(prompt, max_new_tokens=256, do_sample=False)[0]["generated_text"]
    lines = output.splitlines()
    steps: list[str] = []
    for line in lines:
        m = re.match(r"\s*(\d+)[\.)]\s*(.+)", line)
        if m:
            steps.append(m.group(2).strip())
    return steps

def extract_steps(text: str, use_llm: bool = False) -> list[str]:
    """Extract steps using numbering, spaCy, or an optional LLM."""
    if use_llm:
        return llm_extract_steps(text)

    numbered_pattern = re.compile(r"^\s*\d+[\.)]", re.MULTILINE)
    if numbered_pattern.search(text):
        return regex_based_extract_steps(text)
    return semantic_extract_steps(text)

def run(
    in_file: str = "example_input.txt",
    out_file: str = "cleaned_steps.json",
    use_llm: bool = False,
    hf_home: Optional[str] = None,
) -> None:
    """Read the input file, extract steps and save them as JSON.

    If ``hf_home`` is provided via CLI or environment, it is assigned to the
    ``HF_HOME`` variable before loading the optional LLM.
    """
    if hf_home:
        os.environ["HF_HOME"] = hf_home
        os.environ["TRANSFORMERS_CACHE"] = hf_home

    with open(in_file, "r", encoding="utf-8") as f:
        text = f.read()
    steps = extract_steps(text, use_llm=use_llm)
    with open(out_file, "w", encoding="utf-8") as out_f:
        json.dump(steps, out_f, ensure_ascii=False, indent=2)
    print(f"Cleaned steps saved to {out_file}")


def main() -> None:
    """CLI entry point for ``smart-step-extract``."""
    parser = argparse.ArgumentParser(
        description="Extract simplified steps from a Turkish process text."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default="example_input.txt",
        help="Text file containing the raw process description.",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="cleaned_steps.json",
        help="Destination JSON file for the extracted steps.",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Use the Kocdigital LLM instead of spaCy",
    )
    parser.add_argument(
        "--hf-home",
        metavar="PATH",
        help="Directory to use as HF_HOME for cached models",
    )
    args = parser.parse_args()
    run(args.input_file, args.output_file, args.llm, args.hf_home)

if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
