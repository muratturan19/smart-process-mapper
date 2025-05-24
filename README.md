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
