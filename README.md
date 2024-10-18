<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

<h2 align="center">
[ UPDATE v2.10 ]

Dodano funkcję automatycznego pomijania intr i outr w ustawieniach!

</h2>

---


[showcase.webm](https://github.com/user-attachments/assets/f720fdad-4643-47ee-8e7f-2f9a2a6fca55)



---

<table align="center">
<tr>
    <th><div style="width:50%">Dostępne funkcje</div></th>
    <th><div style="width:50%">Planowane funkcje</div></th>
</tr>
<tr>
<td>

- Lista anime do obejrzenia,
- Historia oglądania,
- Funkcja następny/poprzedni odcinek,
- Szybka wyszukiwarka,
- Wznawianie oglądania,
- Możliwość ustawienia własnego statusu na discordzie,
- Statystyki,
- Podgląd okładki,
- Pomijanie intr/outr.

</td>
<td>

- Wsparcie większej ilości źródeł,
- Wyświetlanie markerów intr i outr w odtwarzaczu.

</td>
</tr>
</table>

---
<h1 align="center">
    Instalacja:

</h1>

### Wymagagane paczki:
- `mpv`
- `yt-dlp`
- `python3.9+` (z modułem pip oraz venv)

Instalacja wymaganych paczek na Arch:
```bash
sudo pacman -S mpv yt-dlp python3-pip python3-venv
```

Instalacja wymaganych paczek na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv yt-dlp python3-pip python3-venv
```


### Opcjonalne paczki:
- Wyświetlanie okładek: `timg` [ <a href="https://github.com/hzeller/timg">link do timg</a> ]

- Dla wsparcia źródeł z mega.nz: `megatools`  [ <a href="https://megatools.megous.com/">link do megatools</a> ]


### Instalacja w jednej komendzie:
```bash
cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```

### Aktualizacja w jednej komendzie:
> [!IMPORTANT]  
> Jeżeli aktualizujesz doccli z wersji v2.7.X do wyższej zwróć uwagę na opcjonalne paczki!
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src && cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```


### Jak odinstalować:
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src
```


### Jak usunąć `moją listę` oraz `config` (niezalecane, chyba że wymaga tego aktualizacja):
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
<a href="https://discord.gg/FgfSM7bSEK" target="_blank"><img src="https://dcbadge.limes.pink/api/server/https://discord.gg/FgfSM7bSEK" alt="Link do discorda" style="width: 200px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>
<p align="center">
<a href="https://www.buymeacoffee.com/towarzyszfatcat" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 130px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>


---

<div align="center">
    
[![Star History Chart](https://api.star-history.com/svg?repos=TowarzyszFatCat/doccli&type=Date)](https://star-history.com/)

</div>

---

### Using: <a href="https://github.com/mpv-player/mpv">mpv</a>, <a href="https://api.aniskip.com/api-docs">aniskip-api</a>
### Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>
