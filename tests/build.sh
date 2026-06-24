#!/usr/bin/env bash

set -e

cartridge build -s build/example/
cartridge hdr dump bin/ExampleGBA.gba > tests/result/dump-build

diff tests/result/dump-build tests/expected/dump