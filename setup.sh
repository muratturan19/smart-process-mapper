#!/usr/bin/env bash
pip install -r requirements.txt

# Optional local installation of the Turkish spaCy model
if [ -d turkish-spacy-models/tr_core_news_md ]; then
    pip install -e turkish-spacy-models/tr_core_news_md
    python -m spacy link tr_core_news_md tr_core_news_md
else
    echo "Turkish model not installed. Clone turkish-spacy-models if needed."
fi
