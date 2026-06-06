#!/usr/bin/env bash

curl -L https://static.romsgames.net/a202606068c0w40DWa82/output.bin?mediaId=13610&attach=Super%20Mario%20Advance%202%3A%20Super%20Mario%20World.zip -o game.zip
unzip game.zip
ls 'Super Mario Advance 2 - Super Mario World (USA, Australia).gba'
cartridge hrd dump 'Super Mario Advance 2 - Super Mario World (USA, Australia).gba'