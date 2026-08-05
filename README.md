<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a> i nie tylko!
</h1>

<h2 align="center">
<u><b>NAJNOWSZA WERSJA v2.33</b></u>
</h2>

<p align="center">
  <img src="https://i.imgur.com/1WbW3Er.png" width="32%" alt="Menu">
  <img src="https://i.imgur.com/Uzbjjnl.png" width="32%" alt="Na czasie">
  <img src="https://i.imgur.com/7PMYqqP.png" width="32%" alt="Detale">
</p>

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
- Statystyki programu oraz rangi,
- Podgląd okładek oraz opisy tłumaczone na język polski,
- Pobieranie pełnych sezonów, biblioteka offline i auto-odtwarzanie,
- Anime na czasie,
- Wyświetlanie ocen z AniList,
- Pełna integracja z kontem AniList (auto-zapis postępu i statusu),
- Dwustronna synchronizacja "Mojej listy" z zakładką "Plan to Watch" AniList,
- Sprawdzanie dostępności źródeł na żywo.
- Autoupdater windows oraz prosty instalator [BETA]

</td>
<td>

- Wsparcie większej ilości źródeł,
- Pomijanie intr/outr,
- Wyświetlanie markerów intr i outr w odtwarzaczu,
- Pełne wsparcie dla języka angielskiego.

</td>
</tr>
</table>

---

<h1 align="center">
    Historia aktualizacji v2.32.X - v2.33.X:
</h1>

**v2.32:**
- Dodano wsparcie dla wielu źródeł anglojęzycznych z filtrowaniem napisów i dubbingu,
- Całkowicie przebudowano moduł pobierania – dodano menu wyboru języka oraz nazywanie folderów z prefiksami (np. `[PL]`, `[EN Napisy]`, `[EN Dubbing]`),
- Naprawiono wyświetlanie tytułów na pasku okna MPV podczas strumieniowania źródeł,
- Ulepszono pasek postępu pobierania – program potrafi wyświetlić bezpośrednie komunikaty błędów z narzędzia `yt-dlp` (np. przyczyny zablokowania pobierania przez serwer).

**v2.33:**
- **Naprawiono błąd ze złym wyświetlaniem sezonów** (Błąd zgłoszony przez @Bolo121 DC),
- Naprawiono pobieranie gdy seria ma tylko angielskie źródła (Błąd zgłoszony przez @Bolo121 [#27](https://github.com/TowarzyszFatCat/doccli/issues/27)),
- Dodano pełnoprawny instalator (Powinien on rozwiązywać problem zgłoszony przez @Paczek1200 [#26](https://github.com/TowarzyszFatCat/doccli/issues/26))
- [BETA] Autoupdater windows!
<br>

---
<h1 align="center">
    Instalacja Windows:
</h1>

### Jak zainstalować:
1. Pobierz najnowszy instalator (plik `.exe`, np. `InstallDoccli_v2.33.exe`) z zakładki **[Releases](https://github.com/TowarzyszFatCat/doccli/releases)**,
2. Uruchom pobrany plik instalatora,
3. Postępuj zgodnie z instrukcjami instalatora – aplikacja automatycznie wypakuje się do odpowiedniego katalogu, utworzy skróty na Twoim Pulpicie oraz w Menu Start, a także doda `doccli` do zmiennej systemowej PATH,
4. Po zakończeniu instalacji uruchomi się automatyczny skrypt konfiguracyjny, który pobierze i skonfiguruje wymagane zależności systemowe oraz pakiety Pythona,
5. (Opcjonalne) Ustaw [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) jako domyślny terminal – szczegóły poniżej.

> [!TIP]
> Aby wyciągnąć 100% możliwości z interfejsu `doccli`, **zalecam** korzystanie z [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701). 
> 
> Stary systemowy wiersz polecenia (CMD) jest mocno przestarzały i ma duże ograniczenia. Przesiadka na Windows Terminal daje Ci:
> * **Wysoką jakość okładek** – obrazy renderują się poprawnie i płynnie, zamiast zamieniać się w "krzaczki" i znaki ASCII.
> * Pełne wsparcie dla nowoczesnych kolorów.
> * Poprawne wyświetlanie wszystkich ikon i emoji w menu.
> 
> **Jak zainstalować i ustawić jako domyślny?**
> 1. Pobierz Windows Terminal ze Sklepu Microsoft lub wpisz w zwykłej konsoli: `winget install Microsoft.WindowsTerminal`
> 2. Uruchom pobrany **Terminal**.
> 3. Wejdź w **Ustawienia** (skrót `Ctrl + ,`).
> 4. W zakładce *Uruchamianie* znajdź opcję **Domyślna aplikacja terminala** i zmień z *Wybór niech decyduje system Windows* na **Windows Terminal**.
> 5. Kliknij Zapisz. Od teraz każde uruchomienie `doccli` odpali się w nowym, pięknym oknie!

### Możliwe problemy:
- Na windowsie 10 może pojawić się problem z Instalatorem Aplikacji (App Installer), instalator doccli powinien wyświetlić o tym komunikat i otworzyć okno Microsoft Store, w którym należy zaktualizować aplikację a następnie uruchomić instalator ponownie.

### Jak odinstalować:
- Możesz odinstalować program standardowo poprzez menu systemu Windows (*Dodaj lub usuń programy*) lub uruchamiając plik `unins000.exe` znajdujący się w folderze programu (domyślnie: `%LOCALAPPDATA%\Doccli`). Proces ten usunie aplikację oraz jej skróty.
- Configi i ustawienia użytkownika zapisane są w osobnym folderze `%APPDATA%\doccli`, który należy usunąć ręcznie (o ile chcesz wyczyścić całkowicie dane aplikacji).

---
<h1 align="center">
    Instalacja Linux:
</h1>

### Wymagane paczki:
- `mpv`
- `yt-dlp`
- `python3.12+` (z modułem pip oraz venv)
- `chafa`

Instalacja wymaganych paczek na Arch:
```bash
sudo pacman -S mpv yt-dlp python-pip chafa libjxl
```

Instalacja wymaganych paczek na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv yt-dlp python3-pip python3-venv chafa
```

### Opcjonalne paczki:
- Dla wsparcia źródeł z mega.nz: `megatools`  [ <a href="https://megatools.megous.com/">link do megatools</a> ]

### Instalacja w jednej komendzie:
```bash
cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```

### Aktualizacja w jednej komendzie:
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
