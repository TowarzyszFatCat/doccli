#!/bin/bash

if [ "${PWD##*/}" == "doccli" ] ; then
  sudo chmod +x doccli
  sudo cp doccli /usr/local/bin
  
  sudo mkdir /usr/local/bin/doccli_src
  sudo cp * /usr/local/bin/doccli_src
  
  cd /usr/local/bin/doccli_src && sudo python -m venv .venv
  cd /usr/local/bin/doccli_src && sudo .venv/bin/pip install requests pypresence
else
  echo "WEJDZ DO FOLDERU DOCCLI!"
fi
