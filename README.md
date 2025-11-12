# Ciefpsettings Panel v5.1
![Ciefpsettings Panel](https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/preview.jpg)
> **The most complete and user-friendly plugin manager for Enigma2 (OpenATV, OpenPLI, VTI, BlackHole, OpenBH, etc.)**  
> Install, remove, update and manage over **150+ plugins, panels, IPTV tools, softcams and skins** with just a few clicks!

---

### Features

- **One-click installation** of 150+ popular Enigma2 plugins
- **Multi-select** installation (select multiple plugins → install all at once)
- **Smart Plugin Manager** – view and safely remove installed plugins
- **IPK / TAR.GZ / SH Installer** – install local packages from `/tmp`
- **Auto backup & restore** of installed plugin list during updates
- **Automatic update checker** with one-click update
- **Clean, modern GUI** with background images and color-coded buttons
- **Safe deletion** – prevents removal of system plugins and the panel itself
- **Installation logging** → `/tmp/ciefp_install.log`
- **Persistent selection memory** → remembers your choices via `ciefp_installed_plugins.txt`

---

### Supported Images
Tested and fully working on:
- OpenATV (6.4 - 7.5)
- OpenPLI
- BlackHole
- VTI
- OpenBH
- OpenVision
- Egami
- PurE2
- And many more...

---

### Preview

![Main Menu](https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/screenshot1.jpg)
![Plugin Manager](https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/screenshot2.jpg)
![IPK Installer](https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/screenshot3.jpg)

---

### Installation (Recommended)

```bash
wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/installer.sh -O - | /bin/sh
```

> After installation, restart Enigma2 (or reboot receiver).  
> Find **Ciefpsettings Panel** in the plugin menu.

---

### Manual Installation (Advanced)

```bash
opkg update
opkg install python3-requests python3-json
wget https://github.com/ciefp/CiefpsettingsPanel/archive/refs/heads/main.tar.gz -O /tmp/CiefpsettingsPanel.tar.gz
tar -xzf /tmp/CiefpsettingsPanel.tar.gz -C /usr/lib/enigma2/python/Plugins/Extensions/
rm /tmp/CiefpsettingsPanel.tar.gz
```

Then restart Enigma2.

---

### Update Plugin

The panel **automatically checks for updates** on startup.  
Or force update anytime:
```bash
wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/installer.sh -O - | /bin/sh
```

---

### Included Plugin Categories

| Category                  | Examples |
|---------------------------|---------|
| **Ciefp Tools**           | CiefpSettingsDownloader, CiefpBouquetUpdater, CiefpIPTVBouquets |
| **Panels**                | AjPanel, Linuxsat, Levi45Addons, EmilPanel, Tspanel |
| **IPTV Players**          | X-Streamity, JediMakerXtream, E2iPlayer, XCplugin, EStalker |
| **Softcams**              | Oscam, Ncam, CCcam, oscamicam |
| **Skins**                 | Nitro FHD, MetrixFHD, BO-HLALA, Fury HD, XDREAMY |
| **Tools & Utilities**     | IP Audio Pro, OAWeather, FootOnSat, KeyAdder, SubsSupport |

---

### File Locations

- Plugin path: `/usr/lib/enigma2/python/Plugins/Extensions/CiefpsettingsPanel/`
- Installed list: `/usr/lib/enigma2/python/Plugins/Extensions/CiefpsettingsPanel/ciefp_installed_plugins.txt`
- Backup file: `/tmp/ciefp_installed_plugins_backup.txt`
- Log file: `/tmp/ciefp_install.log`

---

### Safety & Notes

- Cannot delete **CiefpsettingsPanel** itself
- System plugins (OpenWebif, EPGImport, etc.) are **protected**
- Always backup your settings before mass installation
- Use **Blue button** → Restart Enigma2 after installations

---

### Changelog

**v5.1** (12.11.2025)
- Added persistent selection memory (remembers checked plugins)
- Improved plugin detection logic
- Better IPK package name extraction
- Enhanced TAR.GZ installation with fallback
- Fixed backup/restore during updates
- Added more panels and IPTV tools
- Improved logging system

---

### Credits

- **Main Developer**: ciefp  
- **Special thanks**: Emil Nabil, biko-73, fairbird, Belfagor2005, MOHAMED_OS, Ham-ahmed  
- **Community**: LinuxSat, Enigma2 Forum, DreamElite

---

### Support & Feedback

Having issues? Found a bug? Want to suggest a plugin?

Open an **Issue** here on GitHub or contact us on:
- [LinuxSat-Support Forum](https://www.linuxsat-support.com)
- Telegram: ciefpsettings
- Facebook: ciefpsettings

---

### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ciefp/CiefpsettingsPanel&type=Date)](https://star-history.com/#ciefp/CiefpsettingsPanel&Date)

---

**Your receiver deserves the best. Install Ciefpsettings Panel today!**
