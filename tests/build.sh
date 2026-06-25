#!/usr/bin/env bash

set -e

cartridge-sdk build -s build/example/
cartridge-sdk hdr dump bin/ExampleGBA.gba > tests/result/dump-build

diff tests/result/dump-build tests/expected/dump