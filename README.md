<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

<h2 align="center">
UPDATE v2.5! Całkowite przepisanie aplikacji!
</h2>

---


https://github.com/TowarzyszFatCat/doccli/assets/68988781/5264bff1-4746-4581-814e-3989f5eb4bf1


---

<table align="center">
<tr>
    <th><div style="width:50%">Dostępne funkcje</div></th>
    <th><div style="width:50%">Planowane funkcje</div></th>
</tr>
<tr>
<td>

- Lista anime do obejrzenia
- Funkcja następny/poprzedni odcinek
- Szybka wyszukiwarka z całą listą dostępnych anime
- Wznawianie oglądania

</td>
<td>

- Status na discordzie
- Integracje

</td>
</tr>
</table>

---
<h1 align="center">
    Jak zainstalować?

</h1>

### Wymagagane paczki:
Aby korzystać z doccli na systemie linux musisz zainstalować `mpv` i `yt-dlp`! Oraz posiadać pythona3.9 lub nowszego (powinien być domyślnie zainstalowany)

Instalacja `mpv` i `yt-dlp` na Arch:
```bash
sudo pacman -S mpv yt-dlp python3-venv
```

Instalacja `mpv` i `yt-dlp` na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv yt-dlp python3-venv
```

### Instalacja:
```bash
cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```

### Jak odinstalować:
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src
```

### Jak usunąć `moją listę` oraz `config`:
```bash
sudo rm ~/.config/doccli/*
```

### Jak uruchomić:
#####
```bash
doccli
```

---
<p align="center">
<a href="https://discord.gg/FgfSM7bSEK" target="_blank"><img src="https://dcbadge.limes.pink/api/server/https://discord.gg/FgfSM7bSEK" alt="Buy Me A Coffee" style="width: 250px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>
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

