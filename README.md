<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

<h2 align="center">
UPDATE v2.0! Dodano exe dla windowsa!
</h2>

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
<h1 align="center">
    Jak zainstalować?
</h1>

## Windows:
Przejdź do zakładki RELEASES znajdującej się po prawej stronie i pobierz najnowszą wersję! <a href="https://github.com/TowarzyszFatCat/doccli/releases/download/v2.0/doccli.zip">LUB KLIKNIJ TUTAJ</a> Po pobraniu wypakuj gdziekolwiek.

---

## Linux:

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
### Using mpv player: <a href="https://github.com/mpv-player/mpv">mpv</a>
### Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>

