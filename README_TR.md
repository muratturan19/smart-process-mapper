💡 Proje Hakkında
Bu Python modülü, serbest biçimli Türkçe süreç açıklamalarını okuyarak sıralı işlem adımlarına dönüştürür.
Amaç: İnsan tarafından yazılmış operasyon betimlemelerini yapılandırılmış veri haline getirmektir.

📂 Girdi
Kullanıcıdan gelen süreç metni bir .txt dosyasına yazılır.
Örneğin:

example_input.txt

css
Kopyala
Düzenle
İlk olarak hammadde kontrolü yapılır.  
Daha sonra karıştırma işlemine geçilir.  
Dolum başlar.  
Etiketleme ve paketleme yapılır.  
En son kalite kontrol yapılır.
🧠 Ne Yapar?
Süreç cümlelerini analiz eder

Anahtar kelimeleri tarar (örn: “karıştır”, “dolum”, “etiket” vb.)

“önce”, “en son” gibi ifadelerle sıralama kurar

Sonuçta her adımı numaralandırır

▶️ Nasıl Kullanılır?
Terminalden çalıştır:

bash
Kopyala
Düzenle
python process_parser.py
Eğer example_input.txt dosyası klasörde varsa, sonucu terminale yazar:

python
Kopyala
Düzenle
[
  {'step': 'İlk olarak hammadde kontrolü yapılır.', 'order': 1},
  {'step': 'Daha sonra karıştırma işlemine geçilir.', 'order': 2},
  ...
]
🔧 Gereksinimler
txt
Kopyala
Düzenle
Python 3.10
Gerekli kütüphaneler: spaCy 3.4.2, numpy 1.23.5 ve thinc 8.1.10.

Streamlit ve diğer bağımlılıkları yüklemek için `pip install -r requirements.txt` komutunu çalıştırın.

🧱 Dosya Yapısı
bash
Kopyala
Düzenle
project/
├── process_parser.py         ← Ana modül
├── example_input.txt         ← Süreç metni girdisi
└── README.md                 ← Bu belge
❓Metni Python’a Nasıl Vereceksin?
🔹 1. Yöntem: Metni .txt dosyasına yaz
Klasörde bir dosya oluştur:

📄 example_input.txt

İçine şunu yaz:

css
Kopyala
Düzenle
İlk olarak hammadde kontrolü yapılır.  
Daha sonra karıştırma işlemine geçilir.  
Dolum başlar.  
Etiketleme ve paketleme yapılır.  
En son kalite kontrol yapılır.
Sonra process_parser.py dosyasını çalıştır.
Kod zaten bu dosyayı okuyacak şekilde ayarlandı:

python
Kopyala
Düzenle
parsed = parse_process("example_input.txt")

### LLM Kullanımı

İsteğe bağlı olarak [KOCDIGITAL/Kocdigital-LLM-8b-v0.1](https://huggingface.co/KOCDIGITAL/Kocdigital-LLM-8b-v0.1) modelini indirirseniz,
Windows başlangıç betiği indirilen ağırlıkları `HF_HOME` değişkeni ile script dizinine oluşturulan `hf_cache` klasörüne kaydeder,
adım çıkarma işlemini LLM ile gerçekleştirmek için şu komutu çalıştırabilirsiniz:

`smart-step-extract` komutunda `--hf-home` parametresi ile önbellek klasörünü
belirtebilirsiniz.

```bash
python semantic_step_extractor.py example_input.txt cleaned_steps.json --llm
```

`--llm` parametresi verilmezse spaCy tabanlı çıkarıcı kullanılır.
