<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

<h2 align="center">
UPDATE v2.0! Dodano exe dla windowsa!
</h2>

---

https://github.com/TowarzyszFatCat/doccli/assets/68988781/8c6307f0-2fb5-4098-8660-0561105ff479

---

<table align="center">
<tr>
    <th><div style="width:50%">Dostępne funkcje</div></th>
    <th><div style="width:50%">Planowane funkcje</div></th>
</tr>
<tr>
<td>

- Discord Rich Presence (status na discordzie, można go włączyć lub wyłączyć)
- Funkcja następny/poprzedni odcinek
- Szybka wyszukiwarka
- Wznawianie oglądania
- Automatyczny wybór jakości

</td>
<td>

- Wsparcie mega.nz
- Integracja z anilist (po obejrzeniu odcinka doda się do twoich obejrzanych itp.)
- Historia oglądania
- Kategorie
- Customowy status na DC
- Customowe opcje dla mpv

</td>
</tr>
</table>

---

<h3 align="center">Aktualnie nie mam czasu na ulepszanie programu. W II połowie maja zabiorę się za naprawienie błędów i dodanie większej ilości wspieranych stron! Bądźcie cierpliwi :P</h3>

---
<h1 align="center">
    Jak zainstalować?
</h1>

## Windows:
Pobierz z zakładki releases najnowszą wersję <a href="https://github.com/TowarzyszFatCat/doccli/releases/download/v2.0/doccli.zip">lub kliknij tutaj.</a> Po pobraniu wypakuj gdziekolwiek.

---

## Linux:

### Wymagagane paczki na linuxie:
Aby korzystać z doccli na systemie linux musisz zainstalować `mpv` i `yt-dlp`! Oraz posiadać pythona3.9 lub nowszego (powinien być domyślnie zainstalowany)

Instalacja `mpv` i `yt-dlp` na Arch:
```bash
sudo pacman -S mpv yt-dlp python3-venv
```

Instalacja `mpv` i `yt-dlp` na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv yt-dlp python3-venv
```

### Jak zainstalować na linuxie:
```bash
git clone https://github.com/TowarzyszFatCat/doccli.git
```
```bash
cd doccli
```
```bash
bash install.sh
```
Jeżeli wszystko przebiegło pomyślnie, możesz usunąć folder.

### Jak odinstalować na linuxie:
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src
```

### Jak uruchomić na linuxie:
#####
```bash
doccli
```

---

<p align="center">
<a href="https://www.buymeacoffee.com/towarzyszfatcat" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 250px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>


---

<div align="center">
    
[![Star History Chart](https://api.star-history.com/svg?repos=TowarzyszFatCat/doccli&type=Date)](https://star-history.com/)

</div>

---

### Using mpv player: <a href="https://github.com/mpv-player/mpv">mpv</a>
### Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>

