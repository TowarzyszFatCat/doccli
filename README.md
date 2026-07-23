<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a> i nie tylko!
</h1>

<h2 align="center">
<u><b>NAJNOWSZA WERSJA v2.30.3</b></u>
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

</td>
<td>

- Wsparcie większej ilości źródeł,
- Pomijanie intr/outr,
- Wyświetlanie markerów intr i outr w odtwarzaczu.

</td>
</tr>
</table>

---

<h1 align="center">
    Historia aktualizacji v2.30.X:
</h1>

**v2.30:**
- Pełna integracja z AniList (automatyczne zapisywanie postępu i oznaczanie zakończonych serii),
- Dwustronna synchronizacja "Mojej listy" z "Plan to Watch" na AniList w tle,
- W pełni natywne wsparcie na Windowsie z automatycznym instalatorem,
- Wielowątkowe sprawdzanie dostępności źródeł na żywo,
- Pobieranie pełnych sezonów wraz z biblioteką offline i trybem oglądania automatycznego,
- Wskaźnik statusu połączenia z kontem AniList w głównym menu,
- Ulepszone sortowanie "Mojej listy" (najnowsze tytuły wyświetlane na samej górze),
- Opisy anime tłumaczone maszynowo na język polski,
- Statystyki programu oraz unikalne rangi na podstawie czasu oglądania,
- Wyświetlanie okładek w pełnej rozdzielczości z dopasowaniem do terminala,
- Liczne poprawki stabilności (m.in. naprawa błędów źródeł oraz obsługa Discord RPC).

**v2.30.1:**
- Rozbudowane menu pobierania z wyborem jakości,
- Możliwość wybrania jakości i sortowanie według jakości.

**v2.30.2:**
- Możliwość wybrania folderu pobierania.

**v2.30.3:**
- Skrót Ctrl + C działa teraz we wszystkich menu jako błyskawiczne Wróć / Anuluj,
- Wyeliminowano lagi przy ładowaniu długich serii – menu wyświetla się błyskawicznie,
- Zlikwidowano lagi przy uruchamianiu się odtwarzacza i wchodzeniu w listy odcinków,
- Program pokazuje teraz dokładną liczbę wydanych odcinków dla serii, które nadal wychodzą,
- Naprawiono wyświetlanie opisów z AniList,
- Dodano opcję Anuluj w menu wyboru jakości pobierania wideo offline,
- Rozbudowa statystyk i integracja statystyk z Anilist,
- Menu historia od teraz pokazuje co zostało odtworzone online a co offline w doccli,
- Menu historia pokazuje teraz historię oglądania z anilist,
- Menu historia pozwala teraz na wybranie danej pozycji i otworzenia dla niej menu z detalami,
- Moja lista wyświetla teraz także serie ze statusem watching,
- Oglądanie poprzednich odcinków serii nie cofa już progresu na Anilist,
- Instalator na Windowsa jest teraz bardziej przyjazny,
- Markery openingów i endingów,
- Nowe menu wznawiania oglądania,
- Sortowanie po gatunku,
- Kalendarz premier,    
- Opcja losowania spośród gatunku,
- Ocenianie bezpośrednio z aplikacji,
<br>

---
<h1 align="center">
    Instalacja Windows:
</h1>

### Jak zainstalować:
1. Pobierz najnowszą wersję Doccli (plik `.zip`) z zakładki **[Releases](https://github.com/TowarzyszFatCat/doccli/releases)**,
2. Wypakuj pliki w dowolne miejsce (np. do folderu Pobrane),
3. Wejdź do wypakowanego folderu i uruchom plik `install.bat`,
4. Instalator automatycznie pobierze wymagane narzędzia (`winget`, `mpv`, `yt-dlp`, `chafa`), skonfiguruje pythona, a na koniec **utworzy skrót z ikoną na Twoim Pulpicie**,
5. (Opcjonalne) Ustaw [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) jako domyślny terminal, jeżeli go nie masz lub nie wiesz jak to zrobić patrz niżej, 
6. Po udanej instalacji, pobrany folder usunie się sam.

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
- Naciśnij kombinację klawiszy `Win + R`, wpisz `%LOCALAPPDATA%\Doccli` i wciśnij Enter. W otwartym folderze znajdziesz plik `uninstall.bat`, który usunie program i skróty z Twojego komputera, ale zostawi ustawienia użytkownika.
- Configi i ustawienia zapisane są w folderze `%APPDATA%\doccli`, który należy usunąć ręcznie (o ile jest taka potrzeba).

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
sudo pacman -S mpv yt-dlp python3-pip python3-venv chafa
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
