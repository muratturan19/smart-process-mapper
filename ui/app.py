import streamlit as st
from semantic_step_extractor import extract_steps
from pyvis.network import Network
import tempfile

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
    with open("example_input.txt", "r", encoding="utf-8") as f:
        text = f.read()

if text:
    steps = extract_steps(text)
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
        st.components.v1.html(html_content, height=500, scrolling=True)

