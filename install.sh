#!/bin/bash

CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

echo -e "${CYAN}Wybierz język instalacji / Choose installation language:${NC}"
echo "1) Polski"
echo "2) English"
read -p "> " lang_choice

if [ "$lang_choice" = "2" ]; then
    MSG_START="       Starting Doccli installation...      "
    MSG_STEP1="[1/5] Checking system packages (mpv, wget)..."
    MSG_STEP2="[2/5] Removing outdated yt-dlp versions..."
    MSG_STEP3="[3/5] Downloading the latest yt-dlp version..."
    MSG_STEP4="[4/5] Configuring program files..."
    MSG_STEP5="[5/5] Configuring Python libraries (this may take a while)..."
    MSG_DONE="[+] Installation completed successfully!"
    MSG_INFO="[i] You can now type the "
    MSG_INFO_CMD="doccli"
    MSG_INFO2=" command in the terminal."
else
    MSG_START="      Rozpoczynam instalację Doccli...      "
    MSG_STEP1="[1/5] Sprawdzam pakiety systemowe (mpv, wget)..."
    MSG_STEP2="[2/5] Usuwam przestarzałe wersje yt-dlp..."
    MSG_STEP3="[3/5] Pobieram najnowszą wersję yt-dlp od twórców..."
    MSG_STEP4="[4/5] Konfiguruję pliki programu..."
    MSG_STEP5="[5/5] Konfiguruję biblioteki Pythona (może to chwilę potrwać)..."
    MSG_DONE="[+] Instalacja zakończona sukcesem!"
    MSG_INFO="[i] Możesz teraz wpisać polecenie "
    MSG_INFO_CMD="doccli"
    MSG_INFO2=" w terminalu."
fi

clear

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}${MSG_START}${NC}"
echo -e "${CYAN}====================================================${NC}\n"

echo -e "${YELLOW}${MSG_STEP1}${NC}"
sudo apt-get update
sudo apt-get install -y mpv wget chafa
echo ""

echo -e "${YELLOW}${MSG_STEP2}${NC}"
sudo apt-get remove -y yt-dlp
echo ""

echo -e "${YELLOW}${MSG_STEP3}${NC}"
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
echo ""

echo -e "${YELLOW}${MSG_STEP4}${NC}"
sudo chmod +x doccli/doccli
sudo mv doccli/doccli /usr/local/bin

sudo mv doccli ~/.doccli_src

sudo chown -R $USER:$USER ~/.doccli_src

find ~/.doccli_src -type d -exec chmod 755 {} \;
find ~/.doccli_src -type f -exec chmod 644 {} \;
echo ""

echo -e "${YELLOW}${MSG_STEP5}${NC}"
cd ~/.doccli_src && python3 -m venv .venv
cd ~/.doccli_src && .venv/bin/pip install requests inquirerpy termcolor pillow deep-translator rich curl-cffi
cd ~/.doccli_src && .venv/bin/pip install https://github.com/qwertyquerty/pypresence/archive/master.zip
echo ""

mkdir -p ~/.config/doccli
if [ ! -f ~/.config/doccli/settings.json ]; then
    if [ "$lang_choice" = "2" ]; then
        echo '{"language": "en"}' > ~/.config/doccli/settings.json
    else
        echo '{"language": "pl"}' > ~/.config/doccli/settings.json
    fi
fi

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN} ${MSG_DONE}${NC}"
echo -e "${BLUE} ${MSG_INFO}${YELLOW}${MSG_INFO_CMD}${BLUE}${MSG_INFO2}${NC}"
echo -e "${GREEN}====================================================${NC}"