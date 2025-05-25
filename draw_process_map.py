import sys
import os
from process_parser import parse_process


def draw_process_graph(input_file: str, output_path: str = "process_map.png") -> None:
    """Generate a PNG visualization of the parsed process steps.

    Parameters
    ----------
    input_file : str
        Path to the text file containing the process description.
    output_path : str, optional
        Desired output PNG file path. Defaults to ``process_map.png``.
    """
    try:
        from graphviz import Digraph
    except ImportError:
        print("graphviz package not found. Please install it to generate the PNG.")
        return

    steps = parse_process(input_file)
    if not steps:
        print("No steps detected. Nothing to draw.")
        return

    dot = Digraph(format="png")

    # Create nodes with numbered labels
    for idx, step in enumerate(steps, 1):
        node_id = f"step{idx}"
        label = f"{idx}. {step['step']}"
        dot.node(node_id, label)

    # Connect nodes sequentially
    for idx in range(1, len(steps)):
        dot.edge(f"step{idx}", f"step{idx + 1}")

    # Render to the specified output path (without extension)
    filename, _ = os.path.splitext(output_path)
    dot.render(filename, cleanup=True)
    print(f"Process map saved to {filename}.png")


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "example_input.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "process_map.png"
    draw_process_graph(in_file, out_file)
