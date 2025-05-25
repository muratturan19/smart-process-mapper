from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
from semantic_step_extractor import extract_steps
from pyvis.network import Network
import tempfile
import matplotlib.pyplot as plt
from matplotlib import patches

st.set_page_config(page_title="Smart Process Mapper")

st.title("Smart Process Mapper")

option = st.radio(
    "Choose input method", ["Upload a file", "Use example_input.txt"]
)

text = ""
if option == "Upload a file":
    uploaded_file = st.file_uploader(
        "Upload a Turkish process description (.txt)", type=["txt"]
    )
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
else:
    example_path = Path(__file__).resolve().parents[1] / "example_input.txt"
    with open(example_path, "r", encoding="utf-8") as f:
        text = f.read()

if text:
    steps = extract_steps(text)
    if not steps:
        st.warning(
            "No steps were extracted. Ensure the spaCy model is installed and the text is a valid Turkish process description."
        )
    st.subheader("Extracted Steps")
    for idx, step in enumerate(steps, 1):
        st.write(f"{idx}. {step}")

    if steps:
        net = Network(height="400px", directed=True)
        for i, step in enumerate(steps, 1):
            net.add_node(i, label=f"{i}. {step}")
            if i > 1:
                net.add_edge(i - 1, i)
        net.repulsion()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            net.save_graph(tmp_file.name)
            html_content = open(tmp_file.name, "r", encoding="utf-8").read()

        output_dir = Path(__file__).resolve().parents[1] / "outputs"
        output_dir.mkdir(exist_ok=True)
        net.save_graph(output_dir / "process_map_interactive.html")

        st.components.v1.html(html_content, height=500, scrolling=True)

        if st.button("Klasik Süreç Akışını Göster"):
            fig_height = max(2, 1.5 * len(steps))
            fig, ax = plt.subplots(figsize=(6, fig_height))
            ax.axis("off")
            for idx, step in enumerate(steps):
                y = -idx * 2.5
                box = patches.FancyBboxPatch(
                    (0.5, y), 5, 1.5, boxstyle="round,pad=0.3", facecolor="lightgray"
                )
                ax.add_patch(box)
                ax.text(3, y + 0.75, f"{idx + 1}. {step}", ha="center", va="center")
                if idx < len(steps) - 1:
                    ax.annotate(
                        "",
                        xy=(3, y - 0.05),
                        xytext=(3, y - 1.0),
                        arrowprops=dict(arrowstyle="->"),
                    )
            ax.set_xlim(0, 6)
            ax.set_ylim(-2.5 * len(steps), 1.5)
            st.pyplot(fig)

