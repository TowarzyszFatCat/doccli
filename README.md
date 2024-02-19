<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

---

https://github.com/TowarzyszFatCat/doccli/assets/68988781/30996888-de48-4891-9a88-60ede955e4c6

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

</td>
<td>

- Wsparcie mega.nz
- Integracja z anilist (po obejrzeniu odcinka doda się do twoich obejrzanych itp.)
- Historia oglądania
- Kategorie
- Customowy status na DC
- Customowe opcje dla mpv

</td>
</tr>
</table>

---
<h1 align="center">
    Jak zainstalować?
</h1>

## Windows:

<br><br>

<div align="left">
<a href="http://www.youtube.com/watch?feature=player_embedded&v=UrzfqMk4fXg">PORADNIK DO INSTALACJI W WERSJI WIDEO</a>
</div>

<br><br>

> [!NOTE]
> Póki co jedyną możliwością zainstalowania programu na Windowsa jest zainstalowanie go poprzez program Scoop lub za pomocą WSL. W przyszłości może się to zmienić!

### 1) Instalacja Scoop:
> Aby zainstalować doccli na windowsie niezbędny jest <a href="https://scoop.sh/">Scoop</a> czyli program do instalacji CLI.
> Możesz to zrobić za pomocą dwóch komend które należy wpisać w <a href="https://www.google.com/search?q=powershell+jak+w%C5%82%C4%85czy%C4%87">POWER SHELLU</a> widocznych w sekcji Quickstart na stronie <a href="https://scoop.sh/">Scoop.sh</a>, które znajdują się także poniżej.
> ```
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

> [!WARNING]
> Jeżeli po wpisaniu komendy wyskoczył ci komunikat do akceptacji wpisz `A` i naciśnij `Enter`, żeby zaoszczędzić sobie potwierdzania każdego procesu.
 
> ```
> Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
> ```


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

> [!NOTE]
> Istnieje także możliwość instalacji programu za pomocą WSL, więcej dowiesz się tutaj:
> <a href="https://learn.microsoft.com/pl-pl/windows/wsl/about">WSL</a>.
> Po instalacji WSL do instalacji używasz komend z zakładki LINUX

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
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src
```

### Jak uruchomić na linuxie:
#####
```bash
doccli
```

---
### Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>
