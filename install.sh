#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo chmod +x $SCRIPT_DIR/doccli
sudo cp $SCRIPT_DIR/doccli /usr/local/bin

sudo mkdir /usr/local/bin/doccli_src
sudo cp $SCRIPT_DIR/* /usr/local/bin/doccli_src

cd /usr/local/bin/doccli_src && sudo python -m venv .venv
cd /usr/local/bin/doccli_src && sudo .venv/bin/pip install requests pypresence

# Remove install files
sudo rm -rf $SCRIPT_DIR