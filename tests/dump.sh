#!/usr/bin/env bash
set -e

cartridge hdr dump ExampleGBA.gba > tests/result/dump-rom

diff tests/expected/dump tests/result/dump-rom
