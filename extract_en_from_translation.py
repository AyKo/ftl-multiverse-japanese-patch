#en \t ja のリストからenを抽出して出力
englishtext = set()
translate_file = open("translate_en_ja.txt", mode='r', encoding="utf8", errors='ignore')
for line in iter(translate_file.readline, ''):
    enja = line.strip().split('\t')
    if len(enja) == 2:
        en, ja = line.strip().split('\t')
    else:
        ja = en
    englishtext.add(en)

with open("extracted_text.txt", "w", encoding="utf8") as f:
    for text in englishtext:
        f.write("\n" + text)