#!/usr/bin/env bash
set -e

cartridge-sdk hdr dump bin/ExampleGBA.gba > tests/result/dump-rom

diff tests/expected/dump tests/result/dump-rom
