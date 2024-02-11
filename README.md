<h3 align="center">
A cli to watch anime from <a href="https://docchi.pl/">docchi</a> with polish subtitles.
</h3>

[demo](https://github.com/TowarzyszFatCat/doccli/assets/68988781/89a5f65c-8aa6-46f0-9e53-887e6a9dee3a)




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

## Uninstall
```bash
sudo rm -rf /usr/local/bin/doccli_src && sudo rm -rf /usr/local/bin/doccli
```
