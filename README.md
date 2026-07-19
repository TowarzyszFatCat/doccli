<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

<h2 align="center">
<u><b>Co nowego w UPDATE v2.20 - v2.21 ?</b><br></br></u>

W pełni natywne wsparcie na Windowsie z automatycznym instalatorem!<br>
Sprawdzanie dostępności źródeł!</br>
Pobieranie pełnych sezonów!<br>
Przyspieszenie działania wyszukiwarek oraz menu na czasie!<br>
Naprawa błędów odtwarzania z niektórych źródeł.
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
- Pobieranie pełnych sezonów,
- Pomijanie intr/outr, (TYMCZASOWO NIEDOSTĘPNE)
- Anime na czasie,
- Wyświetlanie ocen z Anilist.

</td>
<td>

- Wsparcie większej ilości źródeł,
- Wyświetlanie markerów intr i outr w odtwarzaczu.

</td>
</tr>
</table>

---
<h1 align="center">
    Instalacja Windows:
</h1>

Dzięki nowemu instalatorowi korzystanie z Doccli na systemie Windows jest teraz banalnie proste i nie wymaga używania WSL.

### Jak zainstalować:
1. Pobierz najnowszą wersję Doccli (plik `.zip`) z zakładki **[Releases](https://github.com/TowarzyszFatCat/doccli/releases)**.
2. Wypakuj pliki w dowolne miejsce (np. do folderu Pobrane).
3. Wejdź do wypakowanego folderu i uruchom plik `install.bat`.
4. Instalator automatycznie pobierze wymagane narzędzia (`mpv`, `yt-dlp`), skonfiguruje pythona, a na koniec **utworzy skrót z ikoną na Twoim Pulpicie**.
5. Po udanej instalacji, pobrany folder usunie się sam.

### Jak odinstalować:
Naciśnij kombinację klawiszy `Win + R`, wpisz `%LOCALAPPDATA%\Doccli` i wciśnij Enter. W otwartym folderze znajdziesz plik `uninstall.bat`, który usunie program i skróty z Twojego komputera.

---
<h1 align="center">
    Instalacja Linux:
</h1>

### Wymagane paczki:
- `mpv`
- `yt-dlp`
- `python3.12+` (z modułem pip oraz venv)

Instalacja wymaganych paczek na Arch:
```bash
sudo pacman -S mpv yt-dlp python3-pip python3-venv
```

Instalacja wymaganych paczek na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv yt-dlp python3-pip python3-venv
```

### Opcjonalne paczki:
- Wyświetlanie okładek w lepszej rozdzielczości (tylko niektóre terminale): `timg` [ <a href="https://github.com/hzeller/timg">link do timg</a> ]
- Dla wsparcia źródeł z mega.nz: `megatools`  [ <a href="https://megatools.megous.com/">link do megatools</a> ]

### Instalacja w jednej komendzie:
```bash
cd ~ && git clone [https://github.com/TowarzyszFatCat/doccli.git](https://github.com/TowarzyszFatCat/doccli.git) && bash doccli/install.sh
```

### Aktualizacja w jednej komendzie:
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src && cd ~ && git clone [https://github.com/TowarzyszFatCat/doccli.git](https://github.com/TowarzyszFatCat/doccli.git) && bash doccli/install.sh
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
```bash
doccli
```
---

<h1 align="center">
    Zgłaszanie błędów i propozycje
</h1>

Znalazłeś błąd podczas oglądania? A może masz pomysł na nową, fajną funkcję? Daj mi znać! 
* **Najlepszym i preferowanym sposobem** na zgłoszenie problemu jest otwarcie nowego wątku w zakładce **[Issues na GitHubie](https://github.com/TowarzyszFatCat/doccli/issues)**. 
* Błędy możesz również zgłaszać na serwerze **[Discord](https://discord.gg/FgfSM7bSEK)**, na specjalnie przeznaczonym do tego kanale.

---
<p align="center">
<a href="https://discord.gg/FgfSM7bSEK" target="_blank"><img src="https://dcbadge.limes.pink/api/server/https://discord.gg/FgfSM7bSEK" alt="Link do discorda" style="width: 200px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>
<p align="center">
<a href="https://www.buymeacoffee.com/towarzyszfatcat" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 130px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>

---

<div align="center">
    
[![Star History Chart](https://api.star-history.com/chart?repos=TowarzyszFatCat/doccli&type=date&legend=top-left&sealed_token=qg_zmNfPDW9EpJa3On6tSAKqsvSm4-TkgALKRHmIO0b9jutCjLD2HcI6V6JNCrgJfpzL7Wk_yFSnEfcVazhTWkH5Dcb4YbBP7yb8zML1OfJKWp_rdLqr8w)](https://www.star-history.com/?repos=TowarzyszFatCat%2Fdoccli&type=date&legend=top-left)

</div>

---

### Using: <a href="https://github.com/mpv-player/mpv">mpv</a>, <a href="https://api.aniskip.com/api-docs">aniskip-api</a>
### Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>