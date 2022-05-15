#!/bin/sh
cd $(dirname $0)
mkdir -p output/data
./replace_text_en_ja.py translate_en_ja.txt output/data
cd output
zip -q -r "../FTL-Multiverse 5.2.3 hotfix.jp-patch.zip" data

