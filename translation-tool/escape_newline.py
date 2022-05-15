#!/usr/bin/env python
#
# 改行を"⏎"にする.
#
import sys

print("".join(sys.stdin.readlines()).rstrip().replace('\n', '⏎'))

