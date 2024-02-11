#!/bin/bash

python -m venv doccli_src/.venv
doccli_src/.venv/bin/pip install requests

sudo mv doccli/doccli /usr/local/bin
sudo mv doccli/doccli_src/* /usr/local/bin/doccli_src/

sudo rm -rf doccli
