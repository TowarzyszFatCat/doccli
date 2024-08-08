<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI do oglądania anime z <a href="https://docchi.pl/">docchi.pl</a>
</h1>

<h2 align="center">
[ UPDATE v2.8 ]

Dodano wyświelanie okładek!
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

- Lista anime do obejrzenia
- Historia oglądania
- Funkcja następny/poprzedni odcinek
- Szybka wyszukiwarka z całą listą dostępnych anime
- Wznawianie oglądania 
- Możliwość ustawienia własnego statusu na discordzie
- Statystyki
- Podgląd okładki

</td>
<td>

- Wsparcie większej ilości źródeł

</td>
</tr>
</table>

---

<h1 align="center">
    Instalacja na systemie Windows [Najnowsza: v2.7]:

</h1>

> [!TIP]
> Dla lepszego działania programu zalecane jest korzystanie z Windows Terminal.
> W zwykłym terminalu (cmd) kolory mogą nie być wspierane! Link:
> https://www.microsoft.com/store/productId/9N0DX20HK701?ocid=pdpshare

<h3>Instalacja:</h3>

- Przejdź do zakładki `Releases` lub <a href="https://github.com/TowarzyszFatCat/doccli/releases/latest">kliknij tutaj</a>,
- Pobierz zip zawierający program,
- Wypakuj za pomocą dowolnego narzędzia w dowolnym miejscu (najlepiej pulpit),
- Po pierwszym uruchomieniu program zainstaluje się, a plik `doccli_windows_essentials.zip` powinien zniknąć,
- Po udanej instalacji możesz przenieść `doccli.exe` w dowolne miejsce,
- Koniec!

> [!NOTE]  
> Pliki doccli możesz znaleźć w folderze domowym użytkownika `.config/doccli`


---
<h1 align="center">
    Instalacja na systemie Linux [Najnowsza: v2.8]:

</h1>

### Wymagagane paczki:
Aby korzystać z doccli na systemie linux musisz zainstalować `mpv` i `yt-dlp`! Oraz posiadać pythona3.9 lub nowszego (powinien być domyślnie zainstalowany)

Instalacja `mpv` i `yt-dlp` na Arch:
```bash
sudo pacman -S mpv yt-dlp
```

Instalacja `mpv` i `yt-dlp` na Debian/Ubuntu/Pop:
```bash
sudo apt install mpv yt-dlp
```


> [!WARNING]  
> Na niektórych dystrybucjach wymagana jest także instalacja `python3-venv` przed instalacją doccli!


### Opcjonalne paczki:
Aby wyświetlać okładki wymagana jest instalacja `timg`


### Instalacja w jednej komendzie:
```bash
cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```

### Jak odinstalować:
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src
```

### Aktualizacja w jednej komendzie (połączenie powyższych komend :P):
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src && cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```

> [!IMPORTANT]  
> Jeżeli aktualizujesz doccli z wersji v2.7.X do v2.8 zwróć uwagę na opcjonalne paczki!


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
<a href="https://discord.gg/FgfSM7bSEK" target="_blank"><img src="https://dcbadge.limes.pink/api/server/https://discord.gg/FgfSM7bSEK" alt="Link do discorda" style="width: 250px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
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
