# smart-process-mapper

This project contains a simple parser that extracts ordered process steps from a Turkish text file.
For a Turkish version of this document, see [README_TR.md](README_TR.md).

## Running the parser

Install dependencies and download the Turkish language model before running the parser:

```bash
pip install -r requirements.txt
python -m spacy download tr_core_news_sm
```

Then execute the parser to process the provided `example_input.txt` and write the ordered steps to a JSON file:

```bash
python process_parser.py
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

After obtaining ``cleaned_steps.json`` with ``semantic_step_extractor.py``, you can produce a visual process map using ``draw_process_map.py``:

```bash
python draw_process_map.py cleaned_steps.json
```

The script reads the JSON file and outputs ``process_map.png`` in the current directory. The ``graphviz`` Python package and Graphviz binaries are required for PNG generation.
