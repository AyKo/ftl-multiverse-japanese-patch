#!/usr/bin/env python
#
# Multiverseのdataディレクトリのtextを翻訳版に置き換える.
#
# extract_xml_text.py と translate.sh の結果を第１引数、
# 第２引数に出力先ディレクトリを指定する.
# 
import os
import sys
import xml.etree.ElementTree as ET
import glob
import re

translate_filename = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.isfile(translate_filename):
    os.exit(1)
if not os.path.isdir(output_dir):
    os.exit(2)

special_char_transtable_encode = str.maketrans({
    "\n":"⏎",  # 改行 
    "{":"⛽",  # fule
    "|":"🛫",  # drones
    "}":"🚀",  # missiles
    "~":"💰",  # scrap
    "$":"🔨",  # repair
    "€":"🧑",  # elite
    "‰":"🔥",  # fire
    "†":"💪",  # power
    "‡":"🧊",  # cooldown
    "™":"👆",  # upgraded
})

"""
special_char_transtable_decode = str.maketrans({
    "⏎":"\n",  # 改行 
    "⛽":"{",  # fule
    "🛫":"|",  # drones
    "🚀":"}",  # missiles
    "💰":"~",  # scrap
    "🔨":"$",  # repair
    "🧑":"€",  # elite
    "🔥":"‰",  # fire
    "💪":"†",  # power
    "🧊":"‡",  # cooldown
    "👆":"™",  # upgraded
})
"""

special_char_transtable_decode = str.maketrans({
    "⏎":"\n",  # 改行 
    "⛽":"燃料",  # fule
    "🛫":"ドローン",  # drones
    "🚀":"ミサイル",  # missiles
    "💰":"スクラップ",  # scrap
    "🔨":"$",  # repair
    "🧑":"€",  # elite
    "🔥":"‰",  # fire
    "💪":"†",  # power
    "🧊":"‡",  # cooldown
    "👆":"™",  # upgraded
})

tag_list = ['.//text', './/desc']

translate_map = dict()
translate_file = open(translate_filename, mode='r', encoding="utf8", errors='ignore')
for line in iter(translate_file.readline, ''):
    enja = line.strip().split('\t')
    if len(enja) == 2:
        en, ja = line.strip().split('\t')
    else:
        ja = en
    translate_map[en] = ja

for file in  glob.glob("./data/*"):
    if not os.path.isfile(file):
        continue
    tree = None
    is_change = False
    try: 
        tree = ET.parse(file)
    except ET.ParseError as e:
        continue
    root = tree.getroot()
    for tag in tag_list:
        for texttag in root.findall(tag):
            if not texttag.text:
                continue
            text = re.sub(r'\n[ \t]*', '\n', texttag.text)
            text = text.translate(special_char_transtable_encode)
            if text in translate_map:
                texttag.text = translate_map[text].translate(special_char_transtable_decode)
                is_change = True
    if is_change:
        tree.write(output_dir + "/" + os.path.basename(file), encoding='utf-8')

