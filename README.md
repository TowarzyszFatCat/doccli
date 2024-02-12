<h1 align="center">
A cli to watch anime from <a href="https://docchi.pl/">docchi</a> with polish subtitles.
</h1>

---

[demo](https://github.com/TowarzyszFatCat/doccli/assets/68988781/15160ff1-c184-4ff6-bf04-8a4ea5fa0370)

---

### Future plans:
- [] add exceptions
- [WIP] **windows support**
- [WIP] discord rich presence
- [] streaming from mega.nz
- [] choose player between mpv and vlc
- [] integration with anilist

---

## Dependencies
If you want to use this cli `mpv` and `git` package is needed. You can simply install it by your's system package manager.

##### Example for arch users:
```bash
sudo pacman -S mpv && sudo pacman -S git
```
##### Example for debian/ubuntu users:
```bash
sudo apt install mpv && sudo apt install git
```
---

## Install
#### First clone repo.
```bash
git clone https://github.com/TowarzyszFatCat/doccli.git
```
#### Second execute installation script.
```bash
sh doccli/install.sh
```
> [!WARNING]
> Do not execute script directly from doccli folder, just use command above after cloning repo!

---

## Uninstall
```bash
sudo rm -rf /usr/local/bin/doccli_src && sudo rm -rf /usr/local/bin/doccli
```
---

## Running
##### If you don't now, it's simple, just type this :D
```bash
doccli
```
