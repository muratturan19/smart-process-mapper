pip install -r requirements.txt
pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-any-py3-none-any.whl
python -m spacy link tr_core_news_md tr_core_news_md
