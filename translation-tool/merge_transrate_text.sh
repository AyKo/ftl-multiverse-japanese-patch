#!/bin/bash
#
# 複数の翻訳ファイル(タブ区切りのファイル)、および未翻訳ファイルをマージする.
#
# 1. 同じ翻訳元で未翻訳と翻訳がある場合、未翻訳は出力しない。
# 2. 同じ翻訳元で複数の翻訳があり、かつ同じ翻訳の場合は１つだけ出力する。
# 3. 同じ翻訳元で複数の翻訳があり、かつ異なる翻訳の場合は両方出力する。
#

# 2 を処理
sort -u "$@" |
sort -t '\t' -k 1,1 |
while IFS='\t' read en ja; do
    if [[ "$before_en" == "$en" ]]; then
        if [[ "$before_ja" == "" ]]; then
        fi
    else
    fi
    before_en="$en"
    before_ja="$ja"
done

