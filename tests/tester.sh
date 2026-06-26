#!/usr/bin/env bash

mkdir -p tests/result

bash ./tests/build.sh
bash ./tests/dump.sh
bash ./tests/convert.sh