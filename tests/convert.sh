#!/usr/bin/env bash

set -e

cartridge-sdk conv assets/example/fonts/8x12-bitmap.png -o libs/src/autogenerate/font.c -w 8 -h 12 -m 0 -l 0 -d > tests/result/conv-dump


diff tests/result/conv-dump tests/expected/conv-dump