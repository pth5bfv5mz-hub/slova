#!/usr/bin/env bash
# Пересобирает приложение «Слова» и обновляет ../index.html
set -e
cd "$(dirname "$0")"
cp template.html tmpl.html
for x in audit quiz restore noday cons b1; do python3 patch_$x.py tmpl.html; done
python3 build.py 100
python3 make_index.py
rm -f tmpl.html
