#!/usr/bin/env bash
pip install -r requirements.txt

# Install the Turkish spaCy model
pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-any-py3-none-any.whl
