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


def _build_html_graph(steps: List[str], output_path: str) -> None:
    """Create an interactive HTML process map using ``pyvis``."""
    try:
        from pyvis.network import Network
    except ImportError as exc:  # pragma: no cover - library optional
        raise RuntimeError(
            "pyvis package not found. Please install it to use HTML output."
        ) from exc

    net = Network(height="500px", directed=True)
    for idx, text in enumerate(steps, 1):
        net.add_node(idx, label=f"{idx}. {text}")
        if idx > 1:
            net.add_edge(idx - 1, idx)

    net.write_html(output_path)


def draw_process_graph(
    input_file: str,
    output_path: str = "process_map.png",
    fmt: str = "png",
) -> None:
    """Generate a process map from ``input_file`` in the desired format."""
    try:
        steps = _read_steps(input_file)
    except Exception as exc:  # pragma: no cover - runtime validation
        print(exc)
        return

    try:
        if fmt == "html":
            if output_path.endswith(".png"):
                output_path = os.path.splitext(output_path)[0] + ".html"
            _build_html_graph(steps, output_path)
        else:
            _build_graph(steps, output_path)
            output_path = os.path.splitext(output_path)[0] + ".png"
    except Exception as exc:  # pragma: no cover - runtime validation
        print(f"Failed to render process map: {exc}")
        return

    print(f"Process map saved to {output_path}")


def main() -> None:
    """CLI entry point for the process map generator."""
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
        help="Output file path (PNG or HTML).",
    )
    parser.add_argument(
        "--format",
        choices=["png", "html"],
        default="png",
        help="Output format: png (default) or html for an interactive map.",
    )
    args = parser.parse_args()
    draw_process_graph(args.input_file, args.output_file, args.format)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
