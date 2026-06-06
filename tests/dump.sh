#!/usr/bin/env bash
set -e


cartridge hdr dump tests/Super_Mario_Advance.gba > tests/result/dump-rom

diff tests/expected/dump tests/result/dump-rom
