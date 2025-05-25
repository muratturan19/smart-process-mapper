from typing import List, Dict, Any
import json
import sys
import spacy

try:
    nlp = spacy.load("tr_core_news_sm")
except OSError as exc:
    raise RuntimeError(
        "Turkish spaCy model not found. Run 'python -m spacy download tr_core_news_sm'"
    ) from exc


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


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "example_input.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "parsed_steps.json"
    parse_and_save(in_file, out_file)
