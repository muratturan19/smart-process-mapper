import argparse
import json
import os
from typing import List


def _read_steps(file_path: str) -> List[str]:
    """Return a list of ordered step descriptions from ``file_path``."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Failed to read steps from {file_path}: {exc}") from exc

    if not data:
        raise ValueError("No steps found in input file")

    steps: List[str]
    if all(isinstance(item, dict) for item in data):
        if any("order" in d for d in data):
            data = sorted(data, key=lambda x: x.get("order", 0))
        steps = [d.get("step", "") for d in data if d.get("step")]
    else:
        steps = [str(item) for item in data if str(item)]

    if not steps:
        raise ValueError("Input file did not contain usable steps")

    return steps


def _build_graph(steps: List[str], output_path: str) -> None:
    try:
        from graphviz import Digraph
    except ImportError as exc:
        raise RuntimeError("graphviz package not found. Please install it.") from exc

    dot = Digraph(format="png")
    dot.attr(rankdir="LR", bgcolor="white", pad="0.5", nodesep="0.5", ranksep="0.75")
    dot.attr("node", shape="box", fontname="Arial", fontsize="12", style="rounded,filled")
    dot.attr("edge", arrowsize="0.8", fontname="Arial", fontsize="12")

    for idx, text in enumerate(steps, 1):
        node_id = f"step{idx}"
        label = f"{idx}. {text}"
        if idx == 1:
            color = "lightgreen"
        elif idx == len(steps):
            color = "lightblue"
        else:
            color = "lightgray"
        dot.node(node_id, label, fillcolor=color)

    for idx in range(1, len(steps)):
        dot.edge(f"step{idx}", f"step{idx + 1}")

    filename, _ = os.path.splitext(output_path)
    dot.render(filename, cleanup=True)


def draw_process_graph(input_file: str, output_path: str = "process_map.png") -> None:
    """Generate a styled PNG process map from ``input_file``."""
    try:
        steps = _read_steps(input_file)
    except Exception as exc:  # pragma: no cover - runtime validation
        print(exc)
        return

    try:
        _build_graph(steps, output_path)
    except Exception as exc:  # pragma: no cover - runtime validation
        print(f"Failed to render process map: {exc}")
        return

    out = os.path.splitext(output_path)[0] + ".png"
    print(f"Process map saved to {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a visual process map from a JSON step file."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default="cleaned_steps.json",
        help="JSON file containing ordered or cleaned steps.",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="process_map.png",
        help="Output image file path.",
    )
    args = parser.parse_args()
    draw_process_graph(args.input_file, args.output_file)
