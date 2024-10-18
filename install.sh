#!/bin/bash

sudo chmod +x doccli/doccli
sudo mv doccli/doccli /usr/local/bin

mkdir -p ~/.config/mpv/scripts
sudo mv doccli/doccli-skip.lua ~/.config/mpv/scripts
sudo mv doccli ~/.doccli_src

sudo chmod 777 ~/.doccli_src
sudo chmod 777 ~/.doccli_src/*

cd ~/.doccli_src && sudo python3 -m venv .venv
cd ~/.doccli_src && sudo .venv/bin/pip install requests yt-dlp inquirerpy termcolor
cd ~/.doccli_src && sudo .venv/bin/pip install https://github.com/qwertyquerty/pypresence/archive/master.zip
