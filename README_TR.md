# smart-process-mapper

Bu proje, Türkçe bir metin dosyasından sıralı süreç adımlarını çıkaran basit bir ayrıştırıcı içerir.
Bu belgenin İngilizce sürümü için [README.md](README.md) dosyasına bakın.

## Kurulum

Bu proje yalnızca **Python 3.10** ile test edilmiştir.
Test edilen sürümler spaCy 3.4.2, numpy 1.23.5 ve thinc 8.1.10'dur. Paketi yüklemeden önce Hugging Face'ten Türkçe NLP modelini kurun:
```bash
pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl
pip install -r requirements.txt
pip install .
```

Hem `setup.sh` hem de Windows için `start_ui.bat` betiği modeli aynı URL'den indirir, bu nedenle bu platformlarda manuel kurulum isteğe bağlıdır.

İsteğe bağlı Kocdigital dil modelinden yararlanmak için ağırlıkları `huggingface-cli` kullanarak indirin ve `requirements.txt` içerisindeki `transformers` paketinin kurulu olduğundan emin olun.
Windows başlangıç betiği bu ağırlıkları `HF_HOME` ortam değişkenini ayarlayarak scriptin yanındaki `hf_cache` klasörüne kaydeder.
Alternatif olarak `smart-step-extract` komutunu çalıştırırken `--hf-home` seçeneği ile özel bir önbellek dizini belirtebilirsiniz.

### `HF_HOME` Ayarlama

Hugging Face modelleri `HF_HOME` altında önbelleğe alınır. Komut satırı araçlarını veya `start_ui.bat` dosyasını çalıştırmadan önce özel bir önbellek konumu istiyorsanız bu değişkeni tanımlayın:
```bash
# Windows CMD
set HF_HOME=C:\hf_cache

# PowerShell
$env:HF_HOME="C:\hf_cache"

# Unix shells
export HF_HOME=/path/to/hf_cache
```

Windows batch betiği, scriptin yanındaki yerel `hf_cache` klasöründe Kocdigital LLM dosyaları bulunuyorsa `HF_HOME` ve `TRANSFORMERS_CACHE` değişkenlerini bu klasöre zorla ayarlar. Böylece çevrimdışı çalışırken mevcut `HF_HOME` değeri göz ardı edilir. Ağırlıklar bulunamazsa var olan `HF_HOME` değeri kullanılır (ya da aynı yerel klasör varsayılır).

CLI araçlarını veya Streamlit arayüzünü çalıştırmadan önce `pip install -r requirements.txt` komutunu çalıştırarak tüm bağımlılıkların yüklü olduğundan emin olun.

### Zip arşivi oluşturma

Çevrimdışı bir paket gerekiyorsa, tüm bağımlılıkları ve Hugging Face üzerinden Türkçe spaCy modelini paketlemek için yardımcı betiği çalıştırın:
```bash
bash scripts/build_zip.sh
```

Bu işlem proje dosyalarını ve kurulu kütüphaneleri içeren `dist/smart-process-mapper.zip` dosyasını oluşturur.

### İndirme ve açma

Zip dosyasını sürümler sayfasından indirin veya yukarıdaki gibi kendiniz oluşturun. Ardından arşivi açıp `package` dizininden araçları çalıştırın:
```bash
unzip smart-process-mapper.zip
cd package
python process_parser.py example_input.txt parsed_steps.json
```

## Ayrıştırıcıyı çalıştırmak

Bir metin dosyasından sıralı adımları çıkarmak için:
```bash
smart-process-parse example_input.txt parsed_steps.json
```

Bu komut bulunduğunuz dizinde ``parsed_steps.json`` dosyasını oluşturur.

### Kocdigital LLM kullanımı

İsteğe bağlı [KOCDIGITAL/Kocdigital-LLM-8b-v0.1](https://huggingface.co/KOCDIGITAL/Kocdigital-LLM-8b-v0.1) modeli kuruluysa, adımlar LLM ile spaCy yerine çıkarılabilir:
```bash
smart-step-extract example_input.txt cleaned_steps.json --llm
```

``--llm`` parametresi verilmezse spaCy tabanlı çıkarıcı kullanılır.

``parsed_steps.json`` dosyasının örnek içeriği:
```json
[
  {"step": "Üretim süreci aşağıdaki gibidir: Önce malzemeler karıştırma bölümünde iyice karıştırılır", "order": 1},
  {"step": "Daha sonra karışım dolum makinesine aktarılır ve şişelere doldurulur", "order": 2},
  {"step": "Sonra şişeler etiketleme hattına yönlendirilir", "order": 3},
  {"step": "En son ürünler paketlenerek sevkiyata hazır hale getirilir", "order": 4}
]
```

## Süreç haritası oluşturma

``smart-step-extract`` ile ``cleaned_steps.json`` elde edildikten sonra ``draw-process-map`` komutuyla görsel bir süreç haritası üretebilirsiniz:
```bash
smart-step-extract example_input.txt cleaned_steps.json
draw-process-map cleaned_steps.json
```

Betik JSON dosyasını okuyarak bulunduğunuz dizinde ``process_map.png`` oluşturur. PNG üretimi için ``graphviz`` Python paketi ve Graphviz araçları gereklidir.

Etkileşimli bir HTML sürümü oluşturmak için ``--format html`` parametresini kullanın ve oluşan dosyayı tarayıcıda açın:
```bash
draw-process-map cleaned_steps.json process_map.html --format html
```

Örnek için oluşturulan [process_map.html](process_map.html) dosyasına bakabilirsiniz.

## Streamlit UI'yi çalıştırmak

Etkileşimli bir web arayüzü dahildir. Proje kök dizininden veya `ui` klasörü içinden başlatabilirsiniz:
```bash
streamlit run ui/app.py       # proje kökünden çalıştır
# veya
cd ui
streamlit run app.py          # ui klasöründe çalıştır
```

Windows sistemlerde yalnızca `start_ui.bat` dosyasına çift tıklayarak web arayüzünü başlatabilirsiniz. Betik ilk çalıştırmada yerel bir sanal ortam oluşturur ve gerekli paketleri kurar. Unix kullanıcıları `./start_ui.sh` varsa onu çalıştırabilir ve bağımlılıkları kendileri kurabilir.

## Atıf

`tr_core_news_md` modelini kullanıyorsanız lütfen şu çalışmayı kaynak gösterin:

Altınok, 2023.
