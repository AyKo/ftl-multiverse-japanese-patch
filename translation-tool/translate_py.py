#googeltransを使ってテキストを翻訳 en \t ja で出力
#pip install googletrans==4.0.0rc1
#旧バージョンだとエラー発生
from googletrans import Translator

translator = Translator()

original_text = set()
text_dict = dict()

with open('shortage.txt', 'r' ,encoding='utf8') as f:
    for text in iter(f.readline, ''):
        original_text.add(text)

count = 0
for en in original_text:
    ja = ''
    try :
        ja = translator.translate(en.replace('\n', ''), 'ja', 'en').text
    except :
        print('#error')
    if ja:
        text_dict[en] = ja
        count += 1
        print(f'{count}\t{ja}')

with open('newtext_5.4.1.txt', 'w' ,encoding='utf8') as f:
    for en, ja in text_dict.items():
        f.write(f'\n{en}\t{ja}')

#翻訳に失敗したテキストを出力
fault_text = set()
for text in original_text:
    if not text in text_dict:
        fault_text.add(text)
with open('fault_translation.txt', 'w', encoding='utf8') as f:
    for text in fault_text:
        f.write('\n' + text)
