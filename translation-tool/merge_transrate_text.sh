#!/bin/bash
#
# 複数の翻訳ファイル(タブ区切りのファイル)、および未翻訳ファイルをマージする.
#
#
sort "$@" |
tac |
while IFS=$'\t' read en ja; do
  if [[ "$before_en" == "$en" ]]; then
    if [[ "$before_ja" != "$ja" ]] && [[ "$ja" != "" ]]; then
      printf "%s\t%s\n" "$en" "$ja"
    fi
  else
    printf "%s\t%s\n" "$en" "$ja"
  fi
  before_en="$en"
  before_ja="$ja"
done |
tac

