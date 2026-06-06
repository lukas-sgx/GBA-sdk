#!/usr/bin/env bash

set -e

cartridge build -s build/example/bootstrap.S -o mini.gba
cartridge hdr dump mini.gba > tests/result/dump-build

diff tests/result/dump-build tests/expected/build