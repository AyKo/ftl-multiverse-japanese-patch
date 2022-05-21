#!/usr/bin/env python
#
# data ディレクトリの各ファイルから<text>タグの中身を取り出し、
# 特殊な意味を持つ文字と改行を別の文字に変換後に出力する.
#
import os
import xml.etree.ElementTree as ET
import glob
import re
import sys

# 翻訳で変な変換されないように、特殊な意味をもつ文字を変換するテーブル
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

tag = "text"
if len(sys.argv) > 1:
    tag = sys.argv[1]

# data ディレクトリのすべてのファイルを対象にして..
text_list = set()
for file in  glob.glob("./data/*"):
    if not os.path.isfile(file):
        continue
    tree = None
    # XMLとして読み出し..
    try: 
        tree = ET.parse(file)
    except ET.ParseError as e:
        continue
    root = tree.getroot()
    # <text>タグを探して..
    for texttag in root.findall('.//' + tag):
        if not texttag.text:
            continue
        # 行頭の空白文字は削除し..
        text = re.sub(r'\n[ \t]*', '\n', texttag.text)
        # 文字変換したものを格納（同じものは除外）
        text_list.add(text.translate(special_char_transtable_encode))
# 最後に出力
for text in text_list:
    print(text)

