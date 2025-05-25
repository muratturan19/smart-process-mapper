import argparse
import json
import re
import spacy
import warnings

try:
    nlp = spacy.load("tr_core_news_md")
except OSError:
    warnings.warn(
        "spaCy model 'tr_core_news_md' is not installed. "
        "Install it with "
        "`pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-any-py3-none-any.whl` "
        "and rerun. Falling back to a blank Turkish pipeline."
    )
    nlp = spacy.blank("tr")
    if "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")

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

def extract_steps(text: str) -> list[str]:
    """Extract ordered or semantic steps depending on input format."""
    numbered_pattern = re.compile(r"^\s*\d+[\.)]", re.MULTILINE)
    if numbered_pattern.search(text):
        return regex_based_extract_steps(text)
    return semantic_extract_steps(text)

def main(in_file: str = "example_input.txt", out_file: str = "cleaned_steps.json") -> None:
    """Read the input file, extract steps and save them as JSON."""
    with open(in_file, "r", encoding="utf-8") as f:
        text = f.read()
    steps = extract_steps(text)
    with open(out_file, "w", encoding="utf-8") as out_f:
        json.dump(steps, out_f, ensure_ascii=False, indent=2)
    print(f"Cleaned steps saved to {out_file}")

if __name__ == "__main__":
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
    args = parser.parse_args()
    main(args.input_file, args.output_file)
