# smart-process-mapper

This project contains a simple parser that extracts ordered process steps from a Turkish text file.
For a Turkish version of this document, see [README_TR.md](README_TR.md).

## Installation

Install the package and download the Turkish spaCy model:

```bash
pip install .
python -m spacy download tr_core_news_sm
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
