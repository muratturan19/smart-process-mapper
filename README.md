# smart-process-mapper

This project contains a simple parser that extracts ordered process steps from a Turkish text file.
For a Turkish version of this document, see [README_TR.md](README_TR.md).

## Installation

This project was tested only with **Python 3.10**.
The tested versions are spaCy 3.4.2, numpy 1.23.5 and thinc 8.1.10. Install the Turkish NLP model from Hugging Face before installing this package:
```bash
pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl
pip install -r requirements.txt
pip install .
```

Both `setup.sh` and the Windows launcher `start_ui.bat` fetch the model using
the same URL, so manual installation is optional on those platforms.

To leverage the optional Kocdigital language model, first install the
`transformers` and `huggingface_hub` packages and download the weights with
`python download_model.py`. These dependencies are **not** installed
automatically, so be sure they are available before enabling the LLM features.
The Windows launcher runs this helper automatically when you execute
`start_ui.bat`, storing the snapshot under `hf_cache` by setting the
`HF_HOME` environment variable. If you call the script yourself, define
`HF_HOME` beforehand to choose a custom location. You can also supply the
`--hf-home` option when running `smart-step-extract` to use a different cache
directory.

### Setting `HF_HOME`

Hugging Face models are cached under `HF_HOME`. Define this variable before
running the command-line tools or `start_ui.bat` if you want a custom cache
location:

```bash
# Windows CMD
set HF_HOME=C:\hf_cache

# PowerShell
$env:HF_HOME="C:\hf_cache"

# Unix shells
export HF_HOME=/path/to/hf_cache
```

Always point `HF_HOME` to the **top-level** cache directory. Do not set it to a
subfolder like `hub` or `snapshots`. `start_ui.bat` appends
`hub\models--KOCDIGITAL--Kocdigital-LLM-8b-v0.1` when verifying that the model
weights are present, so pointing `HF_HOME` to one of those subdirectories will
cause the check to fail.

The provided batch script uses the existing `HF_HOME` value when present,
otherwise it defaults to a local `hf_cache` directory.
`TRANSFORMERS_CACHE` is also set to the same location so the Transformers
library can find the cached weights.

Run `pip install -r requirements.txt` before executing the CLI tools or launching the Streamlit UI to ensure all dependencies are available.


### Building a zip archive

If you need an offline bundle, run the helper script to package all
dependencies and the Turkish spaCy model from Hugging Face:

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

### Using the Kocdigital LLM

If the optional [KOCDIGITAL/Kocdigital-LLM-8b-v0.1](https://huggingface.co/KOCDIGITAL/Kocdigital-LLM-8b-v0.1) model is installed and
both `transformers` and `huggingface_hub` are available, steps can be extracted
with the LLM instead of spaCy:

```bash
smart-step-extract example_input.txt cleaned_steps.json --llm
```

Without the ``--llm`` flag the spaCy based extractor is used.

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

An interactive web interface is included. You can start it from the project root or from inside the `ui` directory:

```bash
streamlit run ui/app.py       # run from the project root
# or
cd ui
streamlit run app.py          # run inside the ui folder
```

On Windows systems you can simply double-click `start_ui.bat` to launch the web
interface. The batch script creates a local virtual environment and installs all
required packages on first run. Unix users may run `./start_ui.sh` if the script
is available and handle dependency installation themselves.

## Citation

If you use the `tr_core_news_md` model, please cite:

Altınok, 2023.
