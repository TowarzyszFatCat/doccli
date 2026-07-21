#!/bin/bash

CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}          Rozpoczynam instalację Doccli...          ${NC}"
echo -e "${CYAN}====================================================${NC}\n"

echo -e "${YELLOW}[1/5] Sprawdzam pakiety systemowe (mpv, wget)...${NC}"
sudo apt-get update
sudo apt-get install -y mpv wget chafa
echo ""

echo -e "${YELLOW}[2/5] Usuwam przestarzałe wersje yt-dlp...${NC}"
sudo apt-get remove -y yt-dlp
echo ""

echo -e "${YELLOW}[3/5] Pobieram najnowszą wersję yt-dlp od twórców...${NC}"
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
echo ""

echo -e "${YELLOW}[4/5] Konfiguruję pliki programu...${NC}"
sudo chmod +x doccli/doccli
sudo mv doccli/doccli /usr/local/bin

sudo mv doccli ~/.doccli_src

sudo chown -R $USER:$USER ~/.doccli_src

find ~/.doccli_src -type d -exec chmod 755 {} \;
find ~/.doccli_src -type f -exec chmod 644 {} \;
echo ""

echo -e "${YELLOW}[5/5] Konfiguruję biblioteki Pythona (może to chwilę potrwać)...${NC}"
cd ~/.doccli_src && python3 -m venv .venv
cd ~/.doccli_src && .venv/bin/pip install requests inquirerpy termcolor pillow deep-translator rich
cd ~/.doccli_src && .venv/bin/pip install https://github.com/qwertyquerty/pypresence/archive/master.zip
echo ""

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN} [+] Instalacja zakończona sukcesem!${NC}"
echo -e "${BLUE} [i] Możesz teraz wpisać polecenie ${YELLOW}doccli${BLUE} w terminalu.${NC}"
echo -e "${GREEN}====================================================${NC}"
