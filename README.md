<h1 align="center">
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

---


---
### Zaimplementowane funkcje:
- Sprawdzanie aktualizacji
- Discord rich presence
  ![image](https://github.com/TowarzyszFatCat/doccli/assets/68988781/d4644fc9-3f9f-4181-99d3-3c03d442f74d)

---

### Co może zostać dodane w przyszłości:
- Menu ustawień
- Oglądanie z mega.nz
- Integracja z anilist

---

# Instalacja Windows:

### 1) Instalacja Scoop:
> Aby zainstalować doccli na windowsie niezbędny jest <a href="https://scoop.sh/">Scoop</a> czyli program do instalacji CLI.
> Możesz to zrobić za pomocą dwóch komend które należy wpisać w <a href="https://www.google.com/search?q=powershell+jak+w%C5%82%C4%85czy%C4%87">POWER SHELLU</a> widocznych w sekcji Quickstart na stronie <a href="https://scoop.sh/">Scoop.sh</a>, które znajdują się także poniżej.
> ```
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> ```
> Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
> ```

> [!WARNING]
> Jeżeli po wpisaniu pierwszej komendy wyskoczy ci komunikat do akceptacji wpisz `y` i naciśnij `Enter`

### 2) Dodanie repozytoriów do Scoop i instalacja doccli:
> Za pomocą pobranego wcześniej programu zainstaluj doccli. Wpisując w dowolnym terminalu (np. cmd) te trzy komendy:
> ```
> scoop install git
> ```
> ```
> scoop bucket add extras
> ```
> ^ Po wpisaniu tej komendy naciśnij enter gdy zobaczysz komunikat `Checking repo...`. (możliwe że w innych momentach instalacji też będziesz musiał to zrobić)
> ```
> scoop install https://raw.githubusercontent.com/TowarzyszFatCat/doccli/main/doccli.json
> ```

### 3) Uruchamianie doccli:
> Aby uruchomić doccli w dowolnym terminalu (np. cmd) wpisz:
> ```
> doccli
> ```

> [!WARNING]
> Jeżeli masz jakieś problemy pisz śmiało <a href="https://github.com/TowarzyszFatCat/doccli/issues/new">tutaj</a>.



### Jak zaktualizować:
> [!TIP]
> Pamiętaj aby od czasu do czasu sprawdzać czy nie ma jakiejś aktualizacji :D

> Użyj tej komendy:
> ```
> scoop update doccli
> ```

### Jak odinstalować:
> Wystarczy że odinstalujesz program Scoop. Instrukcję znajdziesz tutaj:
> <a href="https://github.com/ScoopInstaller/Scoop/wiki/Uninstalling-Scoop">Jak odinstalować Scoop</a>.

---
# Instalacja Linux:

### Wymagagane paczki na linuxie:
Aby korzystać z doccli na systemie linux musisz zainstalować `mpv`! Oraz posiadać pythona3.9 lub nowszego (powinien być domyślnie zainstalowany)

Instalacja `mpv` na Arch:
```bash
sudo pacman -S mpv
```

Instalacja `mpv` na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv
```

### Jak zainstalować na linuxie:
```bash
git clone https://github.com/TowarzyszFatCat/doccli.git
```
```bash
sh doccli/install.sh
```

### Jak odinstalować na linuxie:
```bash
sudo rm /usr/local/bin/doccli_src/*
```
```bash
sudo rmdir /usr/local/bin/doccli_src
```
```bash
sudo rm /usr/local/bin/doccli
```

## Jak uruchomić na linuxie:
#####
```bash
doccli
```
---
## Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>
