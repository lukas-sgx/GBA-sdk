#!/usr/bin/env bash

set -e

rm -rf test-init
mkdir test-init
cd test-init
cartridge-sdk init
cartridge-sdk build -s sandbox
ls > ../tests/result/init-dump

diff ../tests/result/init-dump ../tests/expected/init-dump
cd ..
rm -rf test-init