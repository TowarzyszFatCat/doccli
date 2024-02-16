<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

---

https://github.com/TowarzyszFatCat/doccli/assets/68988781/20fc4290-9ef7-48c5-95c8-b9c14292d882

[Kliknij tutaj żeby obejrzeć dłuższy filmik pokazowy](https://youtu.be/GSy1EVMzAbw)

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

</td>
<td>

- Menu ustawień (możliwość konfiguracji programu)
- Wsparcie mega.nz
- Integracja z anilist (po obejrzeniu odcinka doda się do twoich obejrzanych itp.)

</td>
</tr>
</table>

---
<h1 align="center">
    Jak zainstalować?
</h1>

## Windows:

> [!NOTE]
> Póki co jedyną możliwością zainstalowania programu na Windowsa jest zainstalowanie go poprzez Scoop, ponieważ odtwarzacz którego używa program nie jest oficjalnie wspierany na Windowsie. W przyszłości może się to zmienić!

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
> Jeżeli po wpisaniu pierwszej komendy wyskoczy ci komunikat do akceptacji wpisz `A` i naciśnij `Enter`

### 2) Dodanie repozytoriów do Scoop i instalacja doccli:
> Za pomocą pobranego wcześniej programu zainstaluj doccli. Wpisując w dowolnym terminalu (np. cmd) te trzy komendy:
> ```
> scoop install git
> ```
> ```
> scoop bucket add extras
> ```
> ```
> scoop install https://raw.githubusercontent.com/TowarzyszFatCat/doccli/main/doccli.json
> ```

### 3) Uruchamianie doccli:
> Aby uruchomić doccli w dowolnym terminalu (np. cmd) wpisz:
> ```
> doccli
> ```

> [!NOTE]
> Jeżeli nie chcesz otwierać programu za pomocą terminala, możesz w łatwy sposób utworzyć skrót na pulpicie.
> `Prawy przycisk myszy > Nowy > Skrót`
> W polu na lokalizacja elementu wpisz `doccli` i zapisz.
> Możesz też dodać swoją ikonkę wchodząc we właściwości skrótu.


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

## Linux:

### Wymagagane paczki na linuxie:
Aby korzystać z doccli na systemie linux musisz zainstalować `mpv` i `fzf`! Oraz posiadać pythona3.9 lub nowszego (powinien być domyślnie zainstalowany)

Instalacja `mpv` i `fzf` na Arch:
```bash
sudo pacman -S mpv fzf
```

Instalacja `mpv` i `fzf` na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv fzf
```

### Jak zainstalować na linuxie:
```bash
git clone https://github.com/TowarzyszFatCat/doccli.git
```
```bash
cd doccli
```
```bash
sh install.sh
```
Jeżeli wszystko przebiegło pomyślnie, możesz usunąć folder.

### Jak odinstalować na linuxie:
```bash
sudo rm -rf /usr/local/bin/doccli_src && sudo rm /usr/local/bin/doccli
```

### Jak uruchomić na linuxie:
#####
```bash
doccli
```

---
### Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>
