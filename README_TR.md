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

İsteğe bağlı Kocdigital dil modelinden yararlanmak için önce `transformers` ve `huggingface_hub` paketlerini kurup ağırlıkları `python download_model.py` komutuyla indirin. Bu bağımlılıklar otomatik olarak kurulmaz, LLM özelliğini etkinleştirmeden önce mevcut olduklarından emin olun.
`start_ui.bat` çalıştırıldığında bu yardımcı betik otomatik olarak çağrılır ve `HF_HOME` değişkeni `hf_cache` klasörüne ayarlanarak modeller oraya indirilir. Scripti kendiniz çalıştırıyorsanız dosyaların nereye kaydedileceğini belirlemek için `HF_HOME` değerini önceden tanımlayın. 
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

`HF_HOME` her zaman Hugging Face önbellek klasörünün **üst dizinine** işaret etmelidir. `hub` veya `snapshots` gibi alt klasörler kullanılmamalıdır. `start_ui.bat` betiği modeli kontrol ederken `hub\models--KOCDIGITAL--Kocdigital-LLM-8b-v0.1` yolunu eklediği için `HF_HOME`'u bu alt dizinlerden birine yönlendirmek denetimin başarısız olmasına neden olur.

Sağlanan batch betiği var olan `HF_HOME` değerini kullanır, aksi takdirde yerel bir `hf_cache` dizinine varsayılan olarak indirir.
`TRANSFORMERS_CACHE` değişkeni de aynı konuma ayarlanarak Transformers
kütüphanesinin önbelleği doğru yerde aramasını sağlar.

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

İsteğe bağlı [KOCDIGITAL/Kocdigital-LLM-8b-v0.1](https://huggingface.co/KOCDIGITAL/Kocdigital-LLM-8b-v0.1) modeli kurulu ve `transformers` ile `huggingface_hub` paketleri yüklüyse, adımlar LLM ile spaCy yerine çıkarılabilir:
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
