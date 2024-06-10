#!/bin/bash

if [ "${PWD##*/}" == "doccli" ] ; then
  sudo chmod +x doccli
  sudo mv doccli /usr/local/bin
  
  sudo mkdir ~/.doccli_src
  sudo mv * ~/.doccli_src

  sudo chmod 777 ~/.doccli_src
  sudo chmod 777 ~/.doccli_src/*
  
  cd ~/.doccli_src && sudo python3 -m venv .venv
  cd ~/.doccli_src && sudo .venv/bin/pip install requests yt-dlp inquirerpy
else
  echo "WEJDZ DO FOLDERU DOCCLI!"
fi
