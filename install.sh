#!/bin/bash

if [ "${PWD##*/}" == "doccli" ] ; then
  sudo chmod +x doccli
  sudo mv doccli /usr/local/bin
  
  sudo mkdir ~/.doccli_src
  sudo mv * ~/.doccli_src

  sudo chmod 777 ~/.doccli_src
  sudo chmod 777 ~/.doccli_src/*
  sudo chmod 777 ~/.doccli_src/modules/*
  
  cd ~/.doccli_src && sudo python -m venv .venv
  cd ~/.doccli_src && sudo .venv/bin/pip install requests pypresence yt-dlp inquirerpy
else
  echo "WEJDZ DO FOLDERU DOCCLI!"
fi
