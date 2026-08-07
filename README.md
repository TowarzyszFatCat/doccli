<h1 align="center">
<img src="icon_1.png" alt="Icon" width="100" height="100"> <br>
CLI for watching anime!<br>
<a href="README.md"><b>🇬🇧 English</b></a> &nbsp;|&nbsp; <a href="README.pl-PL.md"><b>🇵🇱 Polski</b></a>
</h1>

<h2 align="center">
<u><b>LATEST VERSION v2.40.0</b></u>
</h2>

<p align="center">
  <img src="https://i.imgur.com/JNe5hNG.gif" alt="doccli_gif">
</p>

---

<table align="center">
<tr>
    <th><div style="width:50%">Available Features</div></th>
    <th><div style="width:50%">Planned Features</div></th>
</tr>
<tr>
<td>

- Anime watch list,
- Watch history,
- Next/previous episode feature,
- Quick search engine,
- Resume watching,
- Custom Discord rich presence status,
- Program statistics and ranks,
- Cover previews and descriptions translated into Polish,
- Full season downloading, offline library, and auto-play,
- Trending anime,
- AniList ratings display,
- Full AniList account integration (auto-save progress and status),
- Two-way synchronization of "My List" with AniList's "Plan to Watch" tab,
- Live source availability checking,
- Windows autoupdater and simple installer,
- Notifications about new releases.

</td>
<td>

- Support for more sources,
- Skip intros/outros,
- Display intro and outro markers in the player,

</td>
</tr>
</table>

---

<h1 align="center">
    Update History v2.40.X:
</h1>

**v2.40.0**
- Added full English language support along with an English installer,
- Fixed the autoupdater - it no longer updates in the background, but instead displays a progress window,
- Added an option to randomize anime from my list,
- Resume menu fixes - it now displays the progress of a given series,
- Added a notification system when a new anime episode is released,
- and many more fixes...

---
<h1 align="center">
    Windows Installation:
</h1>

### How to Install:
1. Download the latest installer (`.exe` file, e.g., `InstallDoccli_v2.33.exe`) from the **[Releases](https://github.com/TowarzyszFatCat/doccli/releases)** tab,
2. Run the downloaded installer file,
3. Follow the installer instructions – the application will automatically extract to the appropriate directory, create shortcuts on your Desktop and in the Start Menu, and add `doccli` to the system PATH environment variable,
4. Upon completion, an automatic configuration script will run to download and set up the required system dependencies and Python packages,
5. (Optional) Set [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701) as your default terminal – details below.

> [!TIP]
> To get 100% out of the `doccli` interface, I **recommend** using [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701). 
> 
> The old system Command Prompt (CMD) is heavily outdated and has major limitations. Switching to Windows Terminal gives you:
> * **High cover quality** – images render properly and smoothly instead of turning into "garbled text" and ASCII characters.
> * Full support for modern colors.
> * Proper display of all icons and emojis in the menu.
> 
> **How to install and set as default?**
> 1. Download Windows Terminal from the Microsoft Store or type in a regular console: `winget install Microsoft.WindowsTerminal`
> 2. Open the downloaded **Terminal**.
> 3. Go to **Settings** (shortcut `Ctrl + ,`).
> 4. In the *Startup* tab, find the **Default terminal application** option and change it from *Windows decides* to **Windows Terminal**.
> 5. Click Save. From now on, every launch of `doccli` will open in a new, beautiful window!

### Possible Issues:
- Sometimes you need to run the installer twice because the system doesn't immediately update environment variables.

### How to Uninstall:
- You can uninstall the program standardly through the Windows system menu (*Add or remove programs*) or by running the `unins000.exe` file located in the program folder (default: `%LOCALAPPDATA%\Doccli`). This process will remove the application and its shortcuts.
- User configs and settings are saved in a separate folder `%APPDATA%\doccli`.

---
<h1 align="center">
    Linux Installation:
</h1>

### Required Packages:
- `mpv`
- `yt-dlp`
- `python3.12+` (with pip and venv modules)
- `chafa`

Installing required packages on Arch:
```bash
sudo pacman -S mpv yt-dlp python-pip chafa libjxl
```

Installing required packages on Debian/Ubuntu/Pop:
```bash
sudo apt install mpv yt-dlp python3-pip python3-venv chafa
```

### Optional Packages:
- For mega.nz source support: `megatools`

### Installation in a Single Command:
```bash
cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```

### Update in a Single Command:
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src && cd ~ && git clone https://github.com/TowarzyszFatCat/doccli.git && bash doccli/install.sh
```

### How to Uninstall:
```bash
sudo rm /usr/local/bin/doccli && sudo rm -rf ~/.doccli_src
```

### How to Remove `my list` and `config` (not recommended unless required by an update):
```bash
sudo rm ~/.config/doccli/*
```

### How to Run:
```bash
doccli
```
---

<h1 align="center">
    Bug Reporting and Feature Requests
</h1>

Found a bug while watching? Or maybe you have an idea for a cool new feature? Let me know! 
* **The best and preferred way** to report an issue is by opening a new thread in the **[GitHub Issues](https://github.com/TowarzyszFatCat/doccli/issues)** tab. 
* Bugs can also be reported on the **[Discord](https://discord.gg/FgfSM7bSEK)** server, in a channel specifically designated for this purpose.

---
<p align="center">
<a href="https://discord.gg/FgfSM7bSEK" target="_blank"><img src="https://dcbadge.limes.pink/api/server/https://discord.gg/FgfSM7bSEK" alt="Discord Link" style="width: 200px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>
<p align="center">
<a href="https://www.buymeacoffee.com/towarzyszfatcat" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 130px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
</p>

---

<div align="center">
    
[![Star History Chart](https://api.star-history.com/chart?repos=TowarzyszFatCat/doccli&type=date&legend=top-left&sealed_token=qg_zmNfPDW9EpJa3On6tSAKqsvSm4-TkgALKRHmIO0b9jutCjLD2HcI6V6JNCrgJfpzL7Wk_yFSnEfcVazhTWkH5Dcb4YbBP7yb8zML1OfJKWp_rdLqr8w)]([https://www.star-history.com/?repos=TowarzyszFatCat%2Fdoccli&type=date&legend=top-left](https://www.star-history.com/?repos=TowarzyszFatCat%2Fdoccli&type=date&legend=top-left))

</div>

### Using: <a href="https://github.com/mpv-player/mpv">mpv</a>, <a href="https://api.aniskip.com/api-docs">aniskip-api</a>
### Inspired by: <a href="https://github.com/pystardust/ani-cli">ani-cli</a>
