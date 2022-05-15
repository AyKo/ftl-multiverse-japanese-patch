#!/bin/bash
#
# extract_xml_text.py で作られた翻訳元テキストを翻訳し
#   <翻訳元> <TAB> <翻訳>
# に変換して標準出力する。
# （変換経過が分かるように緑色で標準エラーにも出力している）
#
# 翻訳には trans(1) コマンドを使う.
# Ubuntuなら
#   apt install translate-shell
# でインストールできる.
#

cd $(dirname $0)

MAX_RETRY=5
RANDOM_SLEEP_PARAM_1=5
RANDOM_SLEEP_PARAM_2=5
SOURCE=$1

info() {
    echo -e "$(tput setaf 2)$(date +'%y/%m/%d %H:%M:%S'): $@$(tput sgr0)" >&2
}

warn() {
    echo -e "$(tput setaf 1)$(date +'%y/%m/%d %H:%M:%S'): $@$(tput sgr0)" >&2
}

critical() {
    warn "*CRITICAL* $@"
    exit 1
}

[[ -f "$SOURCE" ]]                 || critical "変換元ファイルを指定してください."
which trans >/dev/null 2>/dev/null || critical "transコマンドがない."

NUM_LINE=$(wc -l < "$SOURCE")

NO=1
cat "$SOURCE" |
while IFS=$'\t' read en_text jp_text; do
    [[ "$en_text" == "" ]] && continue
    RETRY=0
    while [[ "$jp_text" == "" ]]; do
        sleep $((RANDOM % RANDOM_SLEEP_PARAM_2 + RANDOM_SLEEP_PARAM_1 + RETRY * RANDOM_SLEEP_PARAM_2))
        jp_text=$(
            trans -no-ansi -b -s English -t Japanese "$(echo $en_text | ./restore_newline.py)" |
            ./escape_newline.py
        )
        (( RETRY++ ))
        if [[ $RETRY -gt 5 ]]; then
            warn "変換失敗: $en_text"
            jp_text=""
            break
        fi
    done
    printf "%s\t%s\n" "$en_text" "$jp_text"
    info "$NO/$NUM_LINE: 【$en_text】⇒【$jp_text】"
    (( NO++ ))
    unset en_text
    unset jp_text
done

