# smart-process-mapper

This project contains a simple parser that extracts ordered process steps from a Turkish text file.

## Running the parser

Execute the parser directly to process the provided `example_input.txt`:

```bash
python process_parser.py
```

Example output:

```
[{'step': 'Üretim süreci aşağıdaki gibidir: Önce malzemeler karıştırma bölümünde iyice karıştırılır', 'order': 1}, {'step': 'Daha sonra karışım dolum makinesine aktarılır ve şişelere doldurulur', 'order': 2}, {'step': 'Sonra şişeler etiketleme hattına yönlendirilir', 'order': 3}, {'step': 'En son ürünler paketlenerek sevkiyata hazır hale getirilir', 'order': 4}]
```

## Generating a process map

After parsing the text, you can produce a visual process map using `draw_process_map.py`:

```bash
python draw_process_map.py
```

The script reads `example_input.txt` by default and outputs `process_map.png` in the current directory. The `graphviz` Python package and Graphviz binaries are required for PNG generation.
