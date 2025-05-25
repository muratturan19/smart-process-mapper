#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
PKG_DIR="$DIST_DIR/package"

# clean previous build
rm -rf "$DIST_DIR"
mkdir -p "$PKG_DIR"

echo "Installing Python dependencies into $PKG_DIR"
pip install -r "$ROOT_DIR/requirements.txt" --target "$PKG_DIR"

# download Turkish spaCy model
echo "Downloading spaCy model to local package"
python -m spacy download tr_core_news_sm --direct --target "$PKG_DIR"

# copy project scripts
cp "$ROOT_DIR"/*.py "$PKG_DIR"/
cp -r "$ROOT_DIR/ui" "$PKG_DIR/"
cp "$ROOT_DIR/README.md" "$PKG_DIR/"
cp "$ROOT_DIR/README_TR.md" "$PKG_DIR/"
cp "$ROOT_DIR/example_input.txt" "$PKG_DIR/"

cd "$DIST_DIR"
ZIP_NAME="smart-process-mapper.zip"
zip -r "$ZIP_NAME" package

echo "Created $DIST_DIR/$ZIP_NAME"
