pip install -r requirements.txt
pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-1.0-py3-none-any.whl
python -m spacy link tr_core_news_md tr_core_news_md
# Optionally download the KOCDIGITAL LLM weights for offline use
# huggingface-cli download KOCDIGITAL/Kocdigital-LLM-8b-v0.1
