import sys
import os
import json


def draw_process_graph(input_file: str, output_path: str = "process_map.png") -> None:
    """Generate a PNG visualization from cleaned process steps extracted by
    ``semantic_step_extractor.py``.

    Parameters
    ----------
    input_file : str
        Path to the JSON file containing the cleaned steps produced by
        ``semantic_step_extractor.py``.
    output_path : str, optional
        Desired output PNG file path. Defaults to ``process_map.png``.
    """
    try:
        from graphviz import Digraph
    except ImportError:
        print("graphviz package not found. Please install it to generate the PNG.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        steps = json.load(f)
    if not steps:
        print("No steps detected. Nothing to draw.")
        return

    dot = Digraph(format="png")

    # Create nodes with numbered labels
    for idx, step in enumerate(steps, 1):
        node_id = f"step{idx}"
        text = step["step"] if isinstance(step, dict) else step
        label = f"{idx}. {text}"
        dot.node(node_id, label)

    # Connect nodes sequentially
    for idx in range(1, len(steps)):
        dot.edge(f"step{idx}", f"step{idx + 1}")

    # Render to the specified output path (without extension)
    filename, _ = os.path.splitext(output_path)
    dot.render(filename, cleanup=True)
    print(f"Process map saved to {filename}.png")


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "cleaned_steps.json"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "process_map.png"
    draw_process_graph(in_file, out_file)
