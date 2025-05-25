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
        "`pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-any-py3-none-any.whl` "
        "and rerun. Falling back to a blank Turkish pipeline."
    )
    nlp = spacy.blank("tr")
    if "sentencizer" not in nlp.pipe_names:
        nlp.add_pipe("sentencizer")

def extract_steps(text):
    """Extract numbered steps from Turkish process text.

    The function joins lines that belong to the same numeric step and filters
    out blank or extremely short fragments.
    """

    import re

    step_pattern = re.compile(r"^(\d{1,2})\.\s*")
    lines = text.splitlines()

    steps: list[str] = []
    current_parts: list[str] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if step_pattern.match(line):
            if current_parts:
                step_text = " ".join(current_parts).strip()
                if len(step_text.split()) > 1:
                    steps.append(step_text)
            line = step_pattern.sub("", line).strip()
            current_parts = [line]
        else:
            if current_parts:
                current_parts.append(line)

    if current_parts:
        step_text = " ".join(current_parts).strip()
        if len(step_text.split()) > 1:
            steps.append(step_text)

    return steps

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
