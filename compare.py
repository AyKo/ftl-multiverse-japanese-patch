#旧バージョンのテキスト群と新バージョンのdataから抽出したテキストを比較して過不足を出力
import os
import xml.etree.ElementTree as ET
import glob
import re

def ExtractText(multivers_deta_path):
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

    tag_list = ['.//text', './/desc', './/power', './/secretDescription', './/tooltip', './/visitedTooltip', './/unvisitedTooltip', './/crewMember']

    # data ディレクトリのすべてのファイルを対象にして..
    text_list = set()
    for file in  glob.glob(multivers_deta_path + "/data/*"):
        if not os.path.isfile(file):
            continue
        tree = None
        # XMLとして読み出し..
        try: 
            tree = ET.parse(file)
        except ET.ParseError as e:
            print(e)
            continue
        root = tree.getroot()
        # タグを探して..
        for tag in tag_list:
            for texttag in root.findall(tag):
                if not texttag.text:
                    continue
                # 行頭の空白文字は削除し..
                text = re.sub(r'\n[ \t]*', '\n', texttag.text)
                # 文字変換したものを格納（同じものは除外）
                text_list.add(text.translate(special_char_transtable_encode))
    # 最後に出力
    return text_list

#old_text_list = ExtractText("Multiverse 5.3 - Data")
old_text_list = set()
with open("extracted_text.txt", "r", encoding="utf8") as f:
    for text in f.readlines():
        old_text_list.add(text.replace('\n', ''))

new_text_list = ExtractText("Multiverse 5.4.1 - Data")

text_shortage_list = set()
text_surplus_list = set()

for text in new_text_list:
    if not text in old_text_list:
        text_shortage_list.add('\n' + text)
for text in old_text_list:
    if not text in new_text_list:
        text_surplus_list.add('\n' + text)

with open("shortage.txt", "w", encoding="utf8") as shortage:
    for text in text_shortage_list:
        shortage.write(text)
with open("surplus.txt", "w", encoding="utf8") as surplus:
    for text in text_surplus_list:
        surplus.write(text)