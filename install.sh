#!/bin/bash

sudo chmod +x doccli/doccli
sudo mv doccli/doccli /usr/local/bin

sudo mv doccli ~/.doccli_src

sudo chmod 777 ~/.doccli_src
sudo chmod 777 ~/.doccli_src/*

cd ~/.doccli_src && sudo python3 -m venv .venv
cd ~/.doccli_src && sudo .venv/bin/pip install requests yt-dlp inquirerpy termcolor pypresence
