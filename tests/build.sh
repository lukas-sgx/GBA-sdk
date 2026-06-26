#!/usr/bin/env bash

set -e

cartridge-sdk build -s sandbox/
cartridge-sdk hdr dump bin/ExampleGBA.gba > tests/result/dump-build

diff tests/result/dump-build tests/expected/dump