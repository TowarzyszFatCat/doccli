#!/bin/bash

sudo mv doccli/doccli /usr/local/bin
sudo mv doccli/doccli_src /usr/local/bin/
python -m venv /usr/local/bin/doccli_src/.venv
/usr/local/bin/doccli_src/.venv/bin/pip install requests

sudo rm -rf doccli
