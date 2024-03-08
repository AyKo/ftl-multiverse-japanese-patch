#テキストの抽出から翻訳、置換までの一連の関数置き場
#Multiverseのアップデート対応はUpdateMod()を使ってください
import os
import xml.etree.ElementTree as ET
import glob
import re

#翻訳すべきタグリスト
tag_list = ['text', 'desc', 'power', 'secretDescription', 'tooltip', 'visitedTooltip', 'unvisitedTooltip', 'crewMember', 'description']

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

def ExtractText(multivers_file_path: str):
    """マルチバースのフォルダから翻訳すべき英文を抽出する
    
    multiverse_file_path: マルチバースのDataフォルダ(ex:Multiverse 5.4.1 - Data)のパス
    
    =>
    set 翻訳すべき英文のセット
    """
    # data ディレクトリのすべてのファイルを対象にして..
    text_list = set()
    for file in  glob.glob(multivers_file_path + "/data/*"):
        if not os.path.isfile(file):
            continue
        tree = None
        # XMLとして読み出し..
        try: 
            tree = ET.parse(file)
        except ET.ParseError as e:
            continue
        root = tree.getroot()
        # タグを探して..
        for tag in tag_list:
            for texttag in root.findall('.//' + tag):
                if not texttag.text:
                    continue
                # 行頭の空白文字は削除し..
                text = re.sub(r'\n[ \t]*', '\n', texttag.text)
                # 文字変換したものを格納（同じものは除外）
                text_list.add(text.translate(special_char_transtable_encode))
    # 最後に出力
    return text_list

def Compare(old_set: set, new_set: set):
    """#旧バージョンのテキスト群と新バージョンを比較して不足を出力
    
    old_set: 旧バージョンのテキストのセット
    new_set: 新バージョンのテキストのセット
    
    =>
    set: 未翻訳のテキストのセット
    """
    untranslated_text_set = set()
    for text in new_set:
        if not text in old_set:
            untranslated_text_set.add(text)
    return untranslated_text_set
            

def Translation(en_set: set):
    """googeltransを使ってテキストを翻訳
    
    pip install googletrans==4.0.0rc1
    旧バージョンだとエラー発生
    
    en_set: 翻訳すべき英文のセット
    
    =>
    dict {en:ja}の辞書, set 翻訳失敗した英文のセット
    """
    from googletrans import Translator

    translator = Translator()

    en_ja_dict = dict()

    def translation(en):
        for i in range(1, 10):
            try:
                ja = translator.translate(en, 'ja', 'en').text
                return ja
            except:
                pass
        ja = en
        return ja
    
    count = 0
    length = len(en_set)
    for en in en_set:
        ja = translation(en)
        en_ja_dict[en] = ja
        count += 1
        print(f'{count}/{length}\t{ja}')

    #翻訳に失敗したテキストを出力
    fault_text = set()
    for text in en_set:
        if not text in en_ja_dict:
            fault_text.add(text)
    
    return en_ja_dict, fault_text

def MakeEnJaTextFile(enjadict: dict, filename: str):
    """{en:ja}の辞書からen\\tjaテキストを作成し、現在のディレクトリのファイルに格納。
    
    enjadict: {en:ja}の辞書
    filename: 格納するテキストファイル名 ex: en_ja_text.txt
    """
    with open(filename, 'w', encoding='utf8') as f:
        for en, ja in enjadict.items():
            f.write(f'\n{en}\t{ja}')

def MakeEnJaDict(textpath: str):
    """en\\tjaテキストファイルからDictを作る
    
    textpath: en\\tjaテキストファイルのパス
    
    =>
    dict {en:ja}の辞書
    """
    en_ja_dict = dict()
    with open(textpath, 'r', encoding='utf8') as f:
        for line in iter(f.readline, ''):
            enja = line.strip().split('\t')
            if len(enja) == 2:
                en, ja = line.strip().split('\t')
            else:
                ja = en
            en_ja_dict[en] = ja
    return en_ja_dict

def MakeEnSet(textpath: str):
    """en\\tjaテキストファイルからEnのSetを作る
    
    textpath: en\\tjaテキストファイルのパス
    
    =>
    set enのセット
    """
    en_set = set()
    with open(textpath, 'r', encoding='utf8') as f:
        for line in iter(f.readline, ''):
            enja = line.strip().split('\t')
            if len(enja) == 2:
                en, ja = line.strip().split('\t')
            else:
                ja = en
            en_set.add(en)
    return en_set

def Replace(translate_map: dict, input_dir: str, output_dir: str):
    """{en:ja}辞書からMultiverseのdataを日本語版に置換
    
    translate_map: {en:ja}の辞書
    input_dir: 元のマルチバースのDataフォルダ(ex: Multiverse 5.4.1 - Data)のパス
    output_dir: 翻訳版のdataフォルダのパス
    """
    for file in  glob.glob(input_dir + "/data/*"):
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
            for texttag in root.findall('.//' + tag):
                if not texttag.text:
                    continue
                text = re.sub(r'\n[ \t]*', '\n', texttag.text).replace('\t', '')
                text = text.translate(special_char_transtable_encode)
                if text in translate_map:
                    texttag.text = translate_map[text].translate(special_char_transtable_decode)
                    is_change = True
        if is_change:
            tree.write(output_dir + "/data/" + os.path.basename(file), encoding='utf-8')
            
def UpdateMod(new_data_path: str, old_textFile_path: str, ja_mod_folder: str):
    """新しいバージョンのDataと、現バージョンまでのen\\tjaテキストファイルから新しいバージョンの日本語化MODを作る
    new_data_path: 新バージョンのDataファイル(ex: Multiverse 5.4.4 - Data)のパス
    old_textFile_path: en\\tjaのテキストファイルのパス
    ja_mod_folder: Multiverse Japanese Patchのフォルダ
    """
    old_text_set = MakeEnSet(old_textFile_path)
    new_text_set = ExtractText(new_data_path)
    untranslated_text_set = Compare(old_text_set, new_text_set)
    en_ja_dict, failed_text = Translation(untranslated_text_set)
    MakeEnJaTextFile(en_ja_dict, 'new_text.txt')
    if len(failed_text) > 0:
        print('There are some English texts that you failed to translate to Japanese. See \'failed_text.txt\' and continue translation manually.')
        with open('failed_text.txt', 'w', encoding='utf8') as f:
            for text in failed_text:
                f.write(text + '\n')
        return
    else:
        print('All text successfully translated!')
        old_dict = MakeEnJaDict(old_textFile_path)
        old_dict.update(en_ja_dict)
        Replace(old_dict, new_data_path, ja_mod_folder)

if __name__ == '__main__':
    Replace(MakeEnJaDict('AllText(to5.4.4).txt'), 'Multiverse 5.4.4 - Data', r"C:\Users\hulan\OneDrive\デスクトップ\multiverese ja\Multiverse 5.4.4 - Japanese Patch")      
            
def MakeSpreadSheet(wb_id: str, en_ja_dict: dict, multiverse_Data_path: str, credentials_filename_path = 'client_secret.json',authorized_user_filename_path = 'authorized_user.json'):
    """スプレッドシート作成
    
    pip install gspread
    
    wb_id: workbookのid 手を付けていないワークブックを用意してください。
    en_ja_dict: {en:ja}の辞書
    multiverse_Data_path: 元のマルチバースのDataフォルダ(ex: Multiverse 5.4.1 - Data)のパス
    credentials_filename_path: client_secret.jsonのパス
    authorized_user_filename_path: authorized_user.jsonのパス。無い場合は生成
    """
    import gspread

    gc = gspread.oauth(credentials_filename = credentials_filename_path, authorized_user_filename = authorized_user_filename_path)

    wb = gc.open_by_key(wb_id)
    requestlist = []
    titlelist = []

    # data ディレクトリのすべてのファイルを対象にして..
    text_list = set()
    new_id = 0
    for file in  glob.glob(multiverse_Data_path + "/data/*"):
        if not os.path.isfile(file):
            continue
        tree = None
        # XMLとして読み出し..
        try: 
            tree = ET.parse(file)
        except ET.ParseError as e:
            continue
        datalist = [['タグ', '原文', '意訳', '機械翻訳']]
        root = tree.getroot()
        # タグを探して..
        for tag in tag_list:
            for texttag in root.findall('.//' + tag):
                if not texttag.text:
                    continue
                # 行頭の空白文字は削除し..
                text = re.sub(r'\n[ \t]*', '\n', texttag.text)
                text = text.translate(special_char_transtable_encode)
                # 文字変換したものを格納（同じものは除外）
                if text in text_list:
                    continue
                text_list.add(text)
                try:
                    ja = en_ja_dict[text]
                except:
                    ja = text
                datalist.append([f'<{tag}>', text, '', ja])
        data_length = len(datalist)
        if data_length > 1:
            title = os.path.basename(file)
            titlelist.append(title)
            datalist_encode = []
            for arry in datalist:
                row_list = []
                for text in arry:
                    if text:
                        row_list.append({
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP",
                                "verticalAlignment": "TOP",
                            },
                            'userEnteredValue':{
                                'stringValue': text
                            },
                        })
                    else:
                        row_list.append({
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP",
                                "verticalAlignment": "TOP",
                            },
                        })
                datalist_encode.append({
                    'values': row_list,
                })
            new_id += 1
            requestlist.extend([
                {
                    'addSheet':{
                        'properties': {
                            'sheetId': new_id,
                            'title': title,
                            "gridProperties":{
                                "rowCount": data_length,
                                "columnCount": 4,
                            }
                        }
                    },
                },
                {
                    'appendCells':{
                        'sheetId': new_id,
                        'rows': datalist_encode,
                        'fields': 'userEnteredFormat.wrapStrategy, userEnteredFormat.verticalAlignment, userEnteredValue',
                    }
                },
                {
                    'autoResizeDimensions':{
                        "dimensions": {
                            "sheetId": new_id,
                            "dimension": 'ROWS',
                            "startIndex": 1,
                        },
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': new_id,
                            'dimension': 'COLUMNS',
                            'startIndex': 1,
                            'endIndex': 4,
                        },
                        'properties': {
                            'pixelSize': 370,
                        },
                        'fields': 'pixelSize',
                    },
                },
                {
                    'addProtectedRange':{
                        'protectedRange':{
                            'protectedRangeId': new_id,
                            'range': {
                                'sheetId': new_id,
                                'startRowIndex': 1,
                                'endRowIndex': data_length,
                                'startColumnIndex': 0,
                                'endColumnIndex': 1
                            },
                        }
                    }
                }
            ])
    titlelistlength = len(titlelist)
    achievelist = [['シート', '意訳行数', '原文行数', '達成率', '備考'], ['<全体>', '=SUM(B3:B)', '=SUM(C3:C)', '=IFERROR(B2/C2,0)']]
    eachachievelist = [[titlelist[i - 3], f'=COUNTA(INDIRECT(A{i}&"!C2:C"))', f'=COUNTA(INDIRECT(A{i}&"!B2:B"))', f'=IFERROR(B{i}/C{i},0)'] for i in range(3, titlelistlength + 3)]
    achievelist += eachachievelist
    datalist_encode = []
    for arry in achievelist:
        row_list = []
        for text in arry:
            if text[0] == '=':
                row_list.append({
                    "userEnteredFormat": {
                        #"wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                    },
                    'userEnteredValue':{
                        'formulaValue': text
                    },
                })
            else:
                row_list.append({
                    "userEnteredFormat": {
                        #"wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP",
                    },
                    'userEnteredValue':{
                        'stringValue': text
                    },
                })
        datalist_encode.append({
            'values': row_list,
        })
    requestlist.extend([
            {
                'appendCells':{
                    'sheetId': 0,
                    'rows': datalist_encode,
                    'fields': 'userEnteredFormat.wrapStrategy, userEnteredFormat.verticalAlignment, userEnteredValue',
                }
            },
            {
                'addProtectedRange':{
                    'protectedRange':{
                        'protectedRangeId': 0,
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': 1,
                            'endRowIndex': titlelistlength + 2,
                            'startColumnIndex': 0,
                            'endColumnIndex': 4
                        },
                    }
                }
            }
        ])
    wb.batch_update({'requests': requestlist})
