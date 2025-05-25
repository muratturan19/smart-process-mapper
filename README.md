# smart-process-mapper

This project contains a simple parser that extracts ordered process steps from a Turkish text file.
For a Turkish version of this document, see [README_TR.md](README_TR.md).

## Installation

This project is tested with **spaCy 3.7**. Clone the Turkish model repository and install the medium model before installing this package:

```bash
git clone https://github.com/turkish-nlp-suite/turkish-spacy-models
pip install -e turkish-spacy-models/tr_core_news_md
python -m spacy link tr_core_news_md tr_core_news_md
pip install .
```

### Building a zip archive

If you need an offline bundle, run the helper script to package all
dependencies and the Turkish spaCy model:

```bash
bash scripts/build_zip.sh
```

This creates `dist/smart-process-mapper.zip` containing the project files and
installed libraries.

### Download and extraction

Download the zip from the releases page or build it yourself as shown above.
Then extract it and run the tools from the `package` directory:

```bash
unzip smart-process-mapper.zip
cd package
python process_parser.py example_input.txt parsed_steps.json
```

## Running the parser

To extract ordered steps from a text file, run:

```bash
smart-process-parse example_input.txt parsed_steps.json
```

This command creates ``parsed_steps.json`` in the current directory.

Example content of ``parsed_steps.json``:

```json
[
  {"step": "Üretim süreci aşağıdaki gibidir: Önce malzemeler karıştırma bölümünde iyice karıştırılır", "order": 1},
  {"step": "Daha sonra karışım dolum makinesine aktarılır ve şişelere doldurulur", "order": 2},
  {"step": "Sonra şişeler etiketleme hattına yönlendirilir", "order": 3},
  {"step": "En son ürünler paketlenerek sevkiyata hazır hale getirilir", "order": 4}
]
```

## Generating a process map

After obtaining ``cleaned_steps.json`` with ``smart-step-extract``, you can produce a visual process map using ``draw-process-map``:

```bash
smart-step-extract example_input.txt cleaned_steps.json
draw-process-map cleaned_steps.json
```

The script reads the JSON file and outputs ``process_map.png`` in the current directory. The ``graphviz`` Python package and Graphviz binaries are required for PNG generation.

To create an interactive HTML version instead, pass ``--format html`` and open the resulting file in your browser:

```bash
draw-process-map cleaned_steps.json process_map.html --format html
```

See the generated [process_map.html](process_map.html) for an example.

## Running the Streamlit UI

An interactive web interface is included. Launch it with:

```bash
streamlit run ui/app.py
```

Open the URL shown in the terminal to test the extractor in your browser.
