#!/bin/sh
cd $(dirname $0)
./replace_text_en_ja.py translate_en_ja.txt ../data
cd ..
zip -q -r "FTL-Multiverse_5.3.jp-patch.zip" data

