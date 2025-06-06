from typing import List, Dict, Any
import argparse
import json
import spacy
import warnings

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


def parse_process(file_path: str) -> List[Dict[str, Any]]:
    """Parse a Turkish process description file and extract ordered steps."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

    steps = []
    order_counter = 1
    for sent in sentences:
        sent_doc = nlp(sent)
        # action phrase detection via imperative verbs
        if not any(
            tok.pos_ == "VERB" and "Imp" in tok.morph.get("Mood")
            for tok in sent_doc
        ):
            continue

        lemmas = {tok.lemma_.lower() for tok in sent_doc}
        is_before = any(l in {"önce", "ilk"} for l in lemmas)
        is_after = any(l in {"son", "sonra"} for l in lemmas)

        if is_before:
            order_val = 1
            order_counter = max(order_counter, 2)
        elif is_after:
            order_val = 1000  # temporary high value for final step
        else:
            order_val = order_counter
            order_counter += 1

        steps.append({"step": sent, "order": order_val})

    max_order = max((s["order"] for s in steps if s["order"] != 1000), default=0)
    for s in steps:
        if s["order"] == 1000:
            max_order += 1
            s["order"] = max_order

    return sorted(steps, key=lambda x: x["order"])


def parse_and_save(input_file: str, output_file: str = "parsed_steps.json") -> None:
    """Parse the given file and save the ordered steps as JSON.

    Parameters
    ----------
    input_file : str
        Path to the text file containing the raw process description.
    output_file : str, optional
        Destination JSON file. Defaults to ``parsed_steps.json``.
    """
    steps = parse_process(input_file)
    with open(output_file, "w", encoding="utf-8") as out_f:
        json.dump(steps, out_f, ensure_ascii=False, indent=2)
    print(f"Parsed steps saved to {output_file}")


def main() -> None:
    """CLI entry point for ``smart-process-parse``."""
    parser = argparse.ArgumentParser(
        description="Parse a Turkish process description and save ordered steps"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default="example_input.txt",
        help="Path to the text file containing the raw process description.",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="parsed_steps.json",
        help="Destination JSON file for the extracted steps.",
    )
    args = parser.parse_args()
    parse_and_save(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
