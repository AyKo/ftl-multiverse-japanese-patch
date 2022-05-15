#!/usr/bin/env python
#
# "⏎"を改行に戻す.
#
import sys

for line in iter(sys.stdin.readline, ""):
    sys.stdout.write(line.replace('⏎', '\n'))

