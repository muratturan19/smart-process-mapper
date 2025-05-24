from typing import List, Dict, Any
import re


def parse_process(file_path: str) -> List[Dict[str, Any]]:
    """Parse a Turkish process description file and extract ordered steps."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sentences = [s.strip() for s in re.split(r'[\.\n]+', text) if s.strip()]

    steps = []
    order_counter = 1
    for sent in sentences:
        lower = sent.lower()
        # simple keyword check to determine if sentence describes a step
        if any(keyword in lower for keyword in ["karıştır", "dolum", "etiket", "paket"]):
            if "önce" in lower or "ilk" in lower:
                order_val = 1
                order_counter = 2
            elif "en son" in lower:
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


if __name__ == "__main__":
    parsed = parse_process("example_input.txt")
    print(parsed)
