import argparse
import json
import spacy

try:
    nlp = spacy.load("tr_core_news_sm")
except OSError as exc:
    raise RuntimeError(
        "Turkish spaCy model not found. Run 'python -m spacy download tr_core_news_sm'"
    ) from exc

def extract_steps(text):
    """Extract simplified action steps from free-form Turkish process text."""
    doc = nlp(text)
    steps = []
    seen = set()

    for sent in doc.sents:
        for token in sent:
            if token.pos_ != "VERB" or token.dep_ not in {"ROOT", "conj"}:
                continue
            obj = None
            for child in token.children:
                if child.dep_ in {"obj", "obl"} and child.pos_ in {"NOUN", "PROPN"}:
                    obj = child.lemma_
                    break
            # nominalize the verb lemma
            lemma = token.lemma_
            if lemma.endswith("mek") or lemma.endswith("mak"):
                lemma = lemma[:-3] + "me"
            phrase = f"{obj.capitalize() + ' ' if obj else ''}{lemma}"
            if phrase not in seen:
                seen.add(phrase)
                steps.append(phrase)
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
