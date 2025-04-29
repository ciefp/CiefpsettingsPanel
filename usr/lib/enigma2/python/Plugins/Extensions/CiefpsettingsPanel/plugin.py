from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Button import Button
from Components.Pixmap import Pixmap
from enigma import eConsoleAppContainer
from enigma import eTimer
import urllib.request
import json
import os
import logging
import re
import shutil
import glob
import tarfile

# Postavljanje logovanja
logging.basicConfig(filename="/tmp/ciefp_install.log", level=logging.DEBUG, format="%(asctime)s - %(message)s")

# Verzija plugina
PLUGIN_VERSION = "3.4"

# URL za proveru verzije
VERSION_URL = "https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/refs/heads/main/version.txt"

# Fajl za čuvanje instaliranih plugina (perzistentna lokacija)
INSTALLED_PLUGINS_FILE = "/usr/lib/enigma2/python/Plugins/Extensions/CiefpsettingsPanel/ciefp_installed_plugins.txt"

# Privremena lokacija za backup fajla
BACKUP_PLUGINS_FILE = "/tmp/ciefp_installed_plugins_backup.txt"

# Direktorijum za proveru instaliranih plugina
EXTENSIONS_DIR = "/usr/lib/enigma2/python/Plugins/Extensions/"

# Privremeni direktorijum za raspakivanje tar.gz fajlova
TEMP_EXTRACT_DIR = "/tmp/tar_extract/"

# Komanda za ažuriranje plugina
UPDATE_COMMAND = "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/installer.sh -O - | /bin/sh"

# Komande za instalaciju raznih plugina
PLUGINS = {
    "############ ( CiefpSettings Plugins ) ############": "", 
    "CiefpSettingsPanel": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsDownloader": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsDownloader/main/installer.sh -O - | /bin/sh",
    "CiefpsettingsMotor": "wget https://raw.githubusercontent.com/ciefp/CiefpsettingsMotor/main/installer.sh -O - | /bin/sh",
    "CiefpSelectSatellite": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSelectSatellite/main/installer.sh -O - | /bin/sh",
    "CiefpBouquetUpdater": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpBouquetUpdater/main/installer.sh -O - | /bin/sh",
    "CiefpChannelManager": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpChannelManager/main/installer.sh -O - | /bin/sh",
    "CiefpE2Converter": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpE2Converter/main/installer.sh -O - | /bin/sh",
    "CiefpIPTVBouquets": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpIPTVBouquets/main/installer.sh -O - | /bin/sh",
    "CiefpWhitelistStreamrelay": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpWhitelistStreamrelay/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsStreamrelay PY3": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsStreamrelay/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsStreamrelay PY2": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsStreamrelayPY2/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsT2miAbertis": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertis/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsT2miAbertisOpenPLi": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertisOpenPLi/main/installer.sh -O - | /bin/sh",
    "############ ( Panels ) ############": "", 
    "Ciefp-Panel mod Emil Nabil": "wget -q --no-check-certificate https://github.com/emilnabil/download-plugins/raw/refs/heads/main/Ciefp-Panel/Ciefp-Panel.sh -O - | /bin/sh",
    "AjPanel": "wget https://raw.githubusercontent.com/biko-73/AjPanel/main/installer.sh -O - | /bin/sh",
    "Linuxsat Panel": "wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/installer.sh -O - | /bin/sh",
    "Levi45Addons": "wget https://dreambox4u.com/emilnabil237/plugins/levi45-addonsmanager/installer.sh -O - | /bin/sh",
    "SmartAddonsPanel": "wget https://raw.githubusercontent.com/emilnabil/download-plugins/refs/heads/main/SmartAddonspanel/smart-Panel.sh -O - | /bin/sh",
    "MagicPanel": "wget -q --no-check-certificate https://gitlab.com/h-ahmed/Panel/-/raw/main/MagicPanel-install.sh -O - | /bin/sh",
    "ElieSat Panel": "wget -q --no-check-certificate https://gitlab.com/eliesat/extensions/-/raw/main/ajpanel/eliesatpanel.sh -O - | /bin/sh",
    "Panel Lite By Emil Nabil": "wget https://dreambox4u.com/emilnabil237/plugins/ajpanel/new/emil-panel-lite.sh -O - | /bin/sh",
    "Epanel": "wget https://dreambox4u.com/emilnabil237/plugins/epanel/installer.sh -O - | /bin/sh",
    "SatVenusPanel": "wget https://dreambox4u.com/emilnabil237/plugins/satvenuspanel/installer.sh -O - | /bin/sh",
    "Tspanel": "wget https://dreambox4u.com/emilnabil237/plugins/tspanel/installer.sh -O - | /bin/sh",
    "############ ( IPTV Plugins ) ############": "", 
    "X-Streamity": "wget https://raw.githubusercontent.com/biko-73/xstreamity/main/installer.sh -qO - | /bin/sh",
    "XKlass": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/XKlass/online-setup | bash",
    "JediMakerXtream": "wget https://raw.githubusercontent.com/biko-73/JediMakerXtream/main/installer.sh -qO - | /bin/sh",
    "JediEpgExtream": "wget https://dreambox4u.com/emilnabil237/plugins/jediepgextream/installer.sh  -O - | /bin/sh",
    "BouquetMakerXtream": "wget http://dreambox4u.com/emilnabil237/plugins/BouquetMakerXtream/installer.sh -O - | /bin/sh",
    "Vavoo": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Vavoo_Stream/online-setup | bash",
    "vavoo_1.15": "wget https://dreambox4u.com/emilnabil237/plugins/vavoo/installer.sh -O - | /bin/sh", 
    "E2iPlayer": "wget --no-check-certificate https://gitlab.com/MOHAMED_OS/e2iplayer/-/raw/main/install-e2iplayer.sh?inline=false -qO - | /bin/sh",
    "XCplugin": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/XC-Code/installer.sh -qO - | /bin/sh",
    "E2m3u2Bouquet": "wget https://dreambox4u.com/emilnabil237/plugins/e2m3u2bouquet/installer.sh -O - | /bin/sh",
    "HasBahCa": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/HasBahCa/installer.sh -qO - | /bin/sh",
    "PlutoTV": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/PlutoTV/installer.sh -qO - | /bin/sh",
    "Multistalker Pro": "wget -q --no-check-certificate https://dreambox4u.com/emilnabil237/plugins/MultiStalkerPro/installer.sh -O - | /bin/sh",
    "############ ( Plugins ) ############": "", 
    "ONEupdater": "wget https://raw.githubusercontent.com/Sat-Club/ONEupdaterE2/main/installer.sh -O - | /bin/sh",
    "TV Addon": "wget https://dreambox4u.com/emilnabil237/plugins/tvaddon/installer.sh -O - | /bin/sh",
    "RaedQuickSignal": "wget https://raw.githubusercontent.com/fairbird/RaedQuickSignal/main/installer.sh -O - | /bin/sh",
    "KeyAdder": "wget -q --no-check-certificate https://raw.githubusercontent.com/fairbird/KeyAdder/main/installer.sh -O - |/bin/sh",
    "OpenATV softcamfeed": "wget -O - -q http://updates.mynonpublic.com/oea/feed | bash",
    "OpenATV Develop feed": "wget -O - -q https://feeds2.mynonpublic.com/devel-feed | bash",
    "OpenMultiboot_1.3": "wget https://raw.githubusercontent.com/emil237/openmultiboot/main/installer.sh  -O - | /bin/sh",
    "Levi45MulticamManager": "wget https://dreambox4u.com/emilnabil237/plugins/levi45multicammanager/installer.sh -O - | /bin/sh",
    "SubsSupport 1.7.0-r18 Mnasr": "wget -q --no-check-certificate https://github.com/popking159/ssupport/raw/main/subssupport-install.sh -O - | /bin/sh",
    "SubsSupport_1.5.8-r9": "wget https://dreambox4u.com/emilnabil237/plugins/SubsSupport/installer1.sh -O - | /bin/sh", 
    "SubsSupport_2.1": "wget https://dreambox4u.com/emilnabil237/plugins/SubsSupport/subssupport_2.1.sh -O - | /bin/sh",
    "SubsSupport": "wget https://raw.githubusercontent.com/biko-73/SubsSupport/main/installer.sh -qO - | /bin/sh",
    "ChocholousekPicons": "https://github.com/s3n0/e2plugins/raw/master/ChocholousekPicons/online-setup -qO - | bash -s install",
    "The Weather": "wget https://raw.githubusercontent.com/biko-73/TheWeather/main/installer.sh -O - | /bin/sh",
    "Youtube": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/YouTube/installer.sh -qO - | /bin/sh",
    "Aj Panel custom menu": "wget https://raw.githubusercontent.com/biko-73/AjPanel/main/AJPanel_custom_menu_installer.sh -O - | /bin/sh",
    "Plugins by Emil Nabil": "wget --no-check-certificate -O library-plugins.sh https://raw.githubusercontent.com/emil237/download-plugins/main/library-plugins.sh && bash library-plugins.sh",
    "Zip2Pkg by Emil Nabil": "wget https://raw.githubusercontent.com/emilnabil/download-plugins/refs/heads/main/Zip2Pkg/installer.sh -O - | /bin/sh",
    "IP Audio Pro": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/IPaudioPro/online-setup | bash",
    "IP To Sat": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/IPtoSAT/online-setup | bash",
    "XtraEvante": "wget https://github.com/digiteng/xtra/raw/main/xtraEvent.sh -qO - | /bin/sh",
    "E2iPlayer_TSIPlayer": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/E2IPLAYER_TSiplayer/installer.sh -qO - | /bin/sh",
    "FootOnsat": "wget https://raw.githubusercontent.com/ziko-ZR1/FootOnsat/main/Download/install.sh -qO - | /bin/sh",
    "FooTOnSat MOHAMED_OS": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/FootOnsat/online-setup | bash",
    "Simple-Zoom-Panel": "wget https://dreambox4u.com/emilnabil237/plugins/simple-zoom-panel/installer.sh -O - | /bin/sh", 
    "FreeServerCCcam": "wget https://ia803104.us.archive.org/0/items/freecccamserver/installer.sh -qO - | /bin/sh",
    "BissFeedAutoKey": "wget https://raw.githubusercontent.com/emilnabil/bissfeed-autokey/main/installer.sh  -O - | /bin/sh",
    "feeds-finder": "wget https://dreambox4u.com/emilnabil237/plugins/feeds-finder/installer.sh  -O - | /bin/sh",
    "Virtual Keyboard": "wget https://raw.githubusercontent.com/fairbird/NewVirtualKeyBoard/main/installer.sh -O - | /bin/sh",
    "ShootYourScreen-Py3": "wget -q --no-check-certificate https://raw.githubusercontent.com/emil237/ShootYourScreen-Py3/main/ShootYourScreen-py3.sh -O - | /bin/sh",
    "############ ( Softcams ) ############": "", 
    "Oscam Mohamed_OS": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Cam_Emulator/online-setup | bash -s oscam ....... install OSCam Only\n",
    "Ncam Mohamed_OS": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Cam_Emulator/online-setup | bash -s ncam ..... install NCam Only\n",
    "Ncam fairman": "wget https://dreambox4u.com/emilnabil237/emu/installer-ncam.sh -O - | /bin/sh",
    "Oscam Emu biko-73": "wget https://raw.githubusercontent.com/biko-73/OsCam_EMU/main/installer.sh -O - | /bin/sh",
    "Moviecam": "wget https://cutt.ly/Lw6Q9dsi --no-check-certificate -O - | /bin/sh",
    "Cccam": "wget https://dreambox4u.com/emilnabil237/emu/installer-cccam.sh  -O - | /bin/sh",
    "Stalker portal free": "wget -O /home/stalker.conf https://raw.githubusercontent.com/karimSATPRO/Portal-100mag/main/stalker.conf",
    "############ ( Skins ) ############": "", 
    "MADMAX IMPOSSIBLE SKIN OPENATV": "wget https://bit.ly/3cg1664 -qO - | /usr/bin/python",
    "BO-HLALA FHD SKIN": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerB.sh -O - | /bin/sh",
    "Metrix-FHD Skin": "wget http://ipkinstall.ath.cx/ipk-install/MetrixFHD/MetrixFHD.sh -qO - | /bin/sh",
    "Red-Dragon-FHD Skin": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerD.sh -O - | /bin/sh",
    "Nitro AdvanceFHD Skin": "wget https://raw.githubusercontent.com/biko-73/NitroAdvanceFHD/main/installer.sh -qO - | /bin/sh",
    "Desert skin": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerDs.sh -O - | /bin/sh",
    "Fury HD skin": "wget https://raw.githubusercontent.com/islamsalama117/Fury-FHD/refs/heads/main/installer.sh -O - | /bin/sh",
    "XDREAMY skin": "wget -q --no-check-certificate https://raw.githubusercontent.com/Insprion80/Skins/main/xDreamy/installer.sh -O - | /bin/sh",
    "Al Ayam FHD skin": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerAL.sh -O - | /bin/sh",
    "Aglare": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Aglare/online-setup | bash",
    "############ ( Tools ) ############": "", 
    "update": "opkg update",
    "astra-sm": "opkg install astra-sm",
    "reboot": "reboot",
    "restartEnigma2": "killall -9 enigma2",
    "Wget": "opkg install wget",
    "Curl": "opkg install curl",
    "gstplayer": "opkg install gstplayer",
    "Streamlinksrv": "opkg install streamlinksrv",
    "dabstreamer": "opkg install dabstreamer",
    "eti_tools": "opkg install eti-tools",
    "dvbsnoop": "opkg install dvbsnoop",
    "stop enigma2 and network": "init 1",
    "stop enigma2": "init 2",
    "Starts Enigma2 normally": "init 3",
    "stop enigma2": "init 4",
    "stop enigma2": "init 5",
    "Reboots Enigma2": "init 6",
    "Deep Standby": "init 0",
}

class CiefpPluginManager(Screen):
    skin = """
    <screen name="CiefpPluginManager" position="center,center" size="1200,800" title="..:: Ciefp Plugin Manager ::..">
        <!-- Left part for the installed plugins list -->
        <widget name="menu" position="10,10" size="700,650" scrollbarMode="showOnDemand" itemHeight="50" font="Regular;26" />

        <!-- Right part for background image -->
        <widget name="background" position="700,0" size="500,800" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpsettingsPanel/background2.png" zPosition="-1" alphatest="on" />

        <!-- Status at the bottom left -->
        <widget name="status" position="10,720" size="700,30" transparent="1" font="Regular;22" halign="center" />

        <!-- Red button for Delete -->
        <widget name="key_red" position="10,760" size="220,40" font="Bold;22" halign="center" backgroundColor="#9F1313" foregroundColor="#000000" />

        <!-- Green button for Select -->
        <widget name="key_green" position="240,760" size="220,40" font="Bold;22" halign="center" backgroundColor="#1F771F" foregroundColor="#000000" />

        <!-- Blue button for Restart Enigma2 -->
        <widget name="key_blue" position="470,760" size="220,40" font="Bold;22" halign="center" backgroundColor="#13389F" foregroundColor="#000000" />
    </screen>
    """

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        self.installed_plugins = self.load_installed_plugins()
        self["menu"] = MenuList(self.installed_plugins)
        self["background"] = Pixmap()
        self["status"] = Label("Select a plugin with OK or Green, delete with Red")
        self["key_red"] = Button("Red: Delete")
        self["key_green"] = Button("Green: Select")
        self["key_blue"] = Button("Blue: Restart Enigma2")

        self["actions"] = ActionMap(
            ["ColorActions", "SetupActions"],
            {
                "red": self.delete_plugin,
                "green": self.select_plugin,
                "blue": self.restart_enigma2,
                "ok": self.select_plugin,
                "cancel": self.close,
            },
        )

        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.delete_finished)

    def load_installed_plugins(self):
        """Load the list of installed plugins from the log file."""
        if os.path.exists(INSTALLED_PLUGINS_FILE):
            with open(INSTALLED_PLUGINS_FILE, "r") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []

    def save_installed_plugins(self):
        """Save the list of installed plugins to the log file."""
        try:
            with open(INSTALLED_PLUGINS_FILE, "w") as f:
                for plugin in self.installed_plugins:
                    f.write(f"{plugin}\n")
            logging.debug(f"Successfully saved plugins to {INSTALLED_PLUGINS_FILE}")
        except Exception as e:
            logging.error(f"Error saving plugins to {INSTALLED_PLUGINS_FILE}: {str(e)}")
            self["status"].setText(f"Error saving plugins: {str(e)}")

    def find_plugin_folder(self, plugin_name):
        """Pronalazi folder plugina u Extensions direktorijumu, uzimajući u obzir sličnosti."""
        if not os.path.exists(EXTENSIONS_DIR):
            return None

        # Eksplicitna mapa naziva plugina i foldera
        PLUGIN_FOLDER_MAP = {
            "Levi45 Addons Manager": "Levi45Addons",  # Potvrđen tačan naziv foldera
            "TV Addon": "tvaddon",
            "SubsSupport 1.7.0-r18 Mnasr": "SubsSupport",
        }
        if plugin_name in PLUGIN_FOLDER_MAP:
            folder = PLUGIN_FOLDER_MAP[plugin_name]
            if os.path.exists(os.path.join(EXTENSIONS_DIR, folder)):
                return folder

        # Normalizacija naziva plugina
        normalized_name = re.sub(r'[\s\-\_]', '', plugin_name.lower())
        normalized_name = re.sub(r'\d+\.\d+\.\d+.*|r\d+', '', normalized_name)
        for folder in os.listdir(EXTENSIONS_DIR):
            normalized_folder = re.sub(r'[\s\-\_]', '', folder.lower())
            if normalized_folder == normalized_name or folder.lower() == plugin_name.lower():
                return folder
        return None

    def select_plugin(self):
        """Highlight the selected plugin (no additional action for now)."""
        current_index = self["menu"].getSelectionIndex()
        if current_index < len(self.installed_plugins):
            self["status"].setText(f"Selected: {self.installed_plugins[current_index]}")
        else:
            self["status"].setText("No plugin selected")

    def delete_plugin(self):
        """Delete the selected plugin after confirmation."""
        current_index = self["menu"].getSelectionIndex()
        if current_index >= len(self.installed_plugins):
            self["status"].setText("No plugin selected for deletion!")
            return

        plugin = self.installed_plugins[current_index]
        folder_name = self.find_plugin_folder(plugin)

        if not folder_name:
            logging.warning(f"Plugin {plugin} not found in {EXTENSIONS_DIR}")
            self.session.openWithCallback(
                lambda confirmed: self.confirm_delete(plugin, None, confirmed),
                MessageBox,
                f"Plugin {plugin} directory not found. Remove from list?",
                MessageBox.TYPE_YESNO
            )
            return

        # Prikazivanje potvrde za brisanje
        message = f"Do you want to delete the plugin = {folder_name}?"
        self.session.openWithCallback(
            lambda confirmed: self.confirm_delete(plugin, folder_name, confirmed),
            MessageBox,
            message,
            MessageBox.TYPE_YESNO
        )

    def confirm_delete(self, plugin, folder_name, confirmed):
        """Izvršava brisanje ako je korisnik potvrdio."""
        current_index = self["menu"].getSelectionIndex()
        if confirmed:
            if folder_name:
                plugin_path = os.path.join(EXTENSIONS_DIR, folder_name)
                logging.debug(f"Attempting to delete plugin directory: {plugin_path}")
                delete_command = f"sh -c 'rm -rf {plugin_path}'"
                self.container.execute(delete_command)
                # Pokušaj uklanjanja paketa
                os.system(f"opkg remove enigma2-plugin-extensions-{folder_name.lower()}")
            else:
                # Ako folder nije pronađen, samo ukloni iz liste
                logging.debug(f"Removing plugin {plugin} from list (no folder found)")
                del self.installed_plugins[current_index]
                self.save_installed_plugins()
                self["menu"].setList(self.installed_plugins)
                self["status"].setText(f"{plugin} removed from list!")
        else:
            logging.debug(f"Deletion of plugin {plugin} canceled by user")
            self["status"].setText("Deletion canceled")

    def delete_finished(self, retval):
        """Handle completion of plugin deletion."""
        current_index = self["menu"].getSelectionIndex()
        if current_index >= len(self.installed_plugins):
            self["status"].setText("No plugin selected!")
            return

        plugin = self.installed_plugins[current_index]
        if retval == 0:
            logging.debug(f"Successfully deleted plugin: {plugin}")
            self["status"].setText(f"{plugin} deleted successfully!")
            del self.installed_plugins[current_index]
            self.save_installed_plugins()
            self["menu"].setList(self.installed_plugins)
            self.session.open(MessageBox, f"The plugin {plugin} has been deleted. Please restart Enigma manually.", MessageBox.TYPE_INFO, timeout=10)
        else:
            logging.error(f"Error deleting plugin {plugin}, retval: {retval}")
            self["status"].setText(f"Error deleting {plugin}! Check logs.")

    def restart_enigma2(self):
        """Restart Enigma2."""
        self.container.execute("init 4 && init 3")
        self.close()

class IPKInstaller(Screen):
    skin = """
    <screen name="IPKInstaller" position="center,center" size="1600,800" title="..:: IPK and TAR.GZ Installer ::..">
        <!-- Left part for the IPK and TAR.GZ file list -->
        <widget name="menu" position="10,10" size="1080,650" scrollbarMode="showOnDemand" itemHeight="50" font="Regular;26" />

        <!-- Right part for background image -->
        <widget name="background" position="1100,0" size="500,800" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpsettingsPanel/background3.png" zPosition="-1" alphatest="on" />

        <!-- Status at the bottom left -->
        <widget name="status" position="10,720" size="1080,30" transparent="1" font="Regular;22" halign="center" />

        <!-- Red button for Exit -->
        <widget name="key_red" position="10,760" size="250,40" font="Bold;22" halign="center" backgroundColor="#9F1313" foregroundColor="#000000" />

        <!-- Green button for Install IPK -->
        <widget name="key_green" position="270,760" size="250,40" font="Bold;22" halign="center" backgroundColor="#1F771F" foregroundColor="#000000" />

        <!-- Yellow button for Install TAR.GZ -->
        <widget name="key_yellow" position="530,760" size="250,40" font="Bold;22" halign="center" backgroundColor="#9F9F13" foregroundColor="#000000" />

        <!-- Blue button for Restart Enigma2 -->
        <widget name="key_blue" position="790,760" size="250,40" font="Bold;22" halign="center" backgroundColor="#13389F" foregroundColor="#000000" />
    </screen>
    """

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        self.files = self.load_files()
        self["menu"] = MenuList(self.files)
        self["background"] = Pixmap()
        self["status"] = Label("Select a file with OK, install IPK with Green, TAR.GZ with Yellow")
        self["key_red"] = Button("Red: Exit")
        self["key_green"] = Button("Green: Install IPK")
        self["key_yellow"] = Button("Yellow: Install TAR.GZ")
        self["key_blue"] = Button("Blue: Restart Enigma2")

        self["actions"] = ActionMap(
            ["ColorActions", "SetupActions"],
            {
                "red": self.close,
                "green": self.install_ipk,
                "yellow": self.install_tar_gz,
                "blue": self.restart_enigma2,
                "ok": self.select_file,
                "cancel": self.close,
            },
        )

        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.install_finished)

    def load_files(self):
        """Load the list of .ipk and .tar.gz files from /tmp directory."""
        ipk_files = [f"[IPK] {os.path.basename(f)}" for f in glob.glob("/tmp/*.ipk") if os.path.isfile(f)]
        tar_gz_files = [f"[TAR.GZ] {os.path.basename(f)}" for f in glob.glob("/tmp/*.tar.gz") if os.path.isfile(f)]
        all_files = ipk_files + tar_gz_files
        if not all_files:
            self["status"].setText("No IPK or TAR.GZ files found in /tmp")
            return ["No IPK or TAR.GZ files found"]
        return all_files

    def select_file(self):
        """Highlight the selected file."""
        current_index = self["menu"].getSelectionIndex()
        if current_index < len(self.files) and self.files[current_index] != "No IPK or TAR.GZ files found":
            self["status"].setText(f"Selected: {self.files[current_index]}")
        else:
            self["status"].setText("No file selected")

    def get_ipk_package_name(self, ipk_path):
        """Extract the package name from an IPK file."""
        try:
            # Kreiraj privremeni direktorijum za raspakivanje
            temp_dir = "/tmp/ipk_extract/"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)

            # Raspakuj .ipk fajl (to je tar.gz arhiva)
            with tarfile.open(ipk_path, "r:*") as tar:
                tar.extractall(path=temp_dir)

            # Pronađi control.tar.gz i raspakuj ga
            control_tar = None
            for root, _, files in os.walk(temp_dir):
                for f in files:
                    if f == "control.tar.gz":
                        control_tar = os.path.join(root, f)
                        break
                if control_tar:
                    break

            if not control_tar:
                logging.warning(f"No control.tar.gz found in {ipk_path}")
                return None

            with tarfile.open(control_tar, "r:gz") as control:
                control.extractall(path=temp_dir)

            # Pronađi control fajl
            control_file = os.path.join(temp_dir, "control")
            if not os.path.exists(control_file):
                logging.warning(f"No control file found in {ipk_path}")
                shutil.rmtree(temp_dir)
                return None

            # Čitaj Package liniju iz control fajla
            package_name = None
            with open(control_file, "r") as f:
                for line in f:
                    if line.startswith("Package:"):
                        package_name = line.split(":", 1)[1].strip()
                        break

            # Očisti privremeni direktorijum
            shutil.rmtree(temp_dir)

            if package_name:
                # Ako je naziv u formatu enigma2-plugin-extensions-<naziv>, uzmi samo poslednji deo
                if package_name.startswith("enigma2-plugin-extensions-"):
                    package_name = package_name.replace("enigma2-plugin-extensions-", "")
                logging.debug(f"Extracted package name: {package_name} from {ipk_path}")
                return package_name
            else:
                logging.warning(f"No Package field found in control file for {ipk_path}")
                return None

        except Exception as e:
            logging.error(f"Error extracting package name from {ipk_path}: {str(e)}")
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            return None

    def install_ipk(self):
        """Install the selected IPK file."""
        current_index = self["menu"].getSelectionIndex()
        if current_index >= len(self.files) or self.files[current_index] == "No IPK or TAR.GZ files found":
            self["status"].setText("No IPK file selected!")
            return

        file_entry = self.files[current_index]
        if not file_entry.startswith("[IPK]"):
            self["status"].setText("Selected file is not an IPK file!")
            return

        ipk_file = file_entry.replace("[IPK] ", "")
        ipk_path = os.path.join("/tmp", ipk_file)
        if not os.path.exists(ipk_path):
            self["status"].setText(f"File {ipk_file} not found!")
            logging.error(f"IPK file {ipk_path} not found")
            return

        # Izvuci naziv paketa pre instalacije
        package_name = self.get_ipk_package_name(ipk_path)
        if package_name:
            self.current_package_name = package_name  # Sačuvaj za upis nakon instalacije
        else:
            # Fallback: koristi deo imena fajla bez verzije i ekstenzije
            package_name = re.sub(r'[_-]\d+\.\d+\.\d+.*', '', ipk_file).replace('.ipk', '')
            self.current_package_name = package_name
            logging.warning(f"Using fallback package name: {package_name} for {ipk_file}")

        self["status"].setText(f"Installing {ipk_file}...")
        logging.debug(f"Installing IPK file: {ipk_path}")
        install_command = f"opkg install {ipk_path}"
        self.container.execute(install_command)

    def install_tar_gz(self):
        """Install the selected TAR.GZ file."""
        current_index = self["menu"].getSelectionIndex()
        if current_index >= len(self.files) or self.files[current_index] == "No IPK or TAR.GZ files found":
            self["status"].setText("No TAR.GZ file selected!")
            return

        file_entry = self.files[current_index]
        if not file_entry.startswith("[TAR.GZ]"):
            self["status"].setText("Selected file is not a TAR.GZ file!")
            return

        tar_gz_file = file_entry.replace("[TAR.GZ] ", "")
        tar_gz_path = os.path.join("/tmp", tar_gz_file)
        if not os.path.exists(tar_gz_path):
            self["status"].setText(f"File {tar_gz_file} not found!")
            logging.error(f"TAR.GZ file {tar_gz_path} not found")
            return

        self["status"].setText(f"Extracting {tar_gz_file}...")
        logging.debug(f"Extracting TAR.GZ file: {tar_gz_path}")
        try:
            # Kreiraj privremeni direktorijum ako ne postoji
            if os.path.exists(TEMP_EXTRACT_DIR):
                shutil.rmtree(TEMP_EXTRACT_DIR)
            os.makedirs(TEMP_EXTRACT_DIR)

            # Raspakuj tar.gz fajl
            with tarfile.open(tar_gz_path, "r:gz") as tar:
                tar.extractall(path=TEMP_EXTRACT_DIR)

            # Proveri da li postoji očekivana struktura
            extensions_path = os.path.join(TEMP_EXTRACT_DIR, "usr", "lib", "enigma2", "python", "Plugins", "Extensions")
            if os.path.exists(extensions_path):
                # Pronađi naziv plugina
                plugin_name = None
                for item in os.listdir(extensions_path):
                    if os.path.isdir(os.path.join(extensions_path, item)):
                        plugin_name = item
                        break

                if plugin_name:
                    # Kopiraj Extensions direktorijum na sistemsku lokaciju
                    dest_path = os.path.join(EXTENSIONS_DIR, plugin_name)
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                    shutil.copytree(os.path.join(extensions_path, plugin_name), dest_path)
                    logging.debug(f"Copied plugin {plugin_name} to {dest_path}")

                    # Loguj instalirani plugin
                    self.log_installed_plugin(plugin_name)
                    self["status"].setText(f"{tar_gz_file} installed successfully!")
                    self.session.open(MessageBox, f"The TAR.GZ {tar_gz_file} has been installed. Please restart Enigma manually.", MessageBox.TYPE_INFO, timeout=10)
                else:
                    self["status"].setText(f"No plugin directory found in {tar_gz_file}!")
                    logging.error(f"No plugin directory found in {extensions_path}")
            else:
                # Ako nema očekivane strukture, koristi tar xzvf -C /
                self["status"].setText(f"Non-standard TAR.GZ, extracting to root...")
                logging.warning(f"No Extensions directory found in {tar_gz_file}, using tar xzvf -C /")
                self.container.execute(f"tar xzvf {tar_gz_path} -C /")
                return  # Čekaj da se komanda završi pre osvežavanja liste

            # Obriši privremeni direktorijum
            shutil.rmtree(TEMP_EXTRACT_DIR)
            # Osveži listu fajlova
            self.files = self.load_files()
            self["menu"].setList(self.files)

        except Exception as e:
            self["status"].setText(f"Error installing {tar_gz_file}: {str(e)}")
            logging.error(f"Error installing TAR.GZ {tar_gz_file}: {str(e)}")
            if os.path.exists(TEMP_EXTRACT_DIR):
                shutil.rmtree(TEMP_EXTRACT_DIR)

    def log_installed_plugin(self, plugin_name):
        """Log an installed plugin to the file."""
        try:
            plugin_dir = os.path.dirname(INSTALLED_PLUGINS_FILE)
            if not os.path.exists(plugin_dir):
                os.makedirs(plugin_dir)
                logging.debug(f"Created directory: {plugin_dir}")

            existing_plugins = set()
            if os.path.exists(INSTALLED_PLUGINS_FILE):
                with open(INSTALLED_PLUGINS_FILE, "r") as f:
                    existing_plugins = {line.strip() for line in f if line.strip()}

            if plugin_name not in existing_plugins:
                with open(INSTALLED_PLUGINS_FILE, "a") as f:
                    f.write(f"{plugin_name}\n")
                logging.debug(f"Logged plugin {plugin_name} to {INSTALLED_PLUGINS_FILE}")
        except Exception as e:
            logging.error(f"Error logging plugin {plugin_name}: {str(e)}")
            self["status"].setText(f"Error logging plugin {plugin_name}: {str(e)}")

    def install_finished(self, retval):
        """Handle completion of IPK or TAR.GZ installation."""
        current_index = self["menu"].getSelectionIndex()
        if current_index >= len(self.files) or self.files[current_index] == "No IPK or TAR.GZ files found":
            self["status"].setText("No file selected!")
            return

        file_entry = self.files[current_index]
        file_name = file_entry.replace("[IPK] ", "").replace("[TAR.GZ] ", "")
        if file_entry.startswith("[IPK]"):
            if retval == 0:
                logging.debug(f"Successfully installed IPK: {file_name}")
                self["status"].setText(f"{file_name} installed successfully!")
                # Loguj naziv plugina iz .ipk fajla
                if hasattr(self, 'current_package_name') and self.current_package_name:
                    self.log_installed_plugin(self.current_package_name)
                self.session.open(MessageBox, f"The IPK {file_name} has been installed. Please restart Enigma manually.", MessageBox.TYPE_INFO, timeout=10)
            else:
                logging.error(f"Error installing IPK {file_name}, retval: {retval}")
                self["status"].setText(f"Error installing {file_name}! Check logs.")
        elif file_entry.startswith("[TAR.GZ]"):
            if retval == 0:
                logging.debug(f"Successfully installed TAR.GZ: {file_name}")
                self["status"].setText(f"{file_name} installed successfully!")
                self.session.open(MessageBox, f"The TAR.GZ {file_name} has been installed. Please restart Enigma manually.", MessageBox.TYPE_INFO, timeout=10)
            else:
                logging.error(f"Error installing TAR.GZ {file_name}, retval: {retval}")
                self["status"].setText(f"Error installing {file_name}! Check logs.")

        # Osveži listu fajlova
        self.files = self.load_files()
        self["menu"].setList(self.files)

    def restart_enigma2(self):
        """Restart Enigma2."""
        self.container.execute("init 4 && init 3")
        self.close()

class CiefpsettingsPanel(Screen):
    skin = """
    <screen name="CiefpsettingsPanel" position="center,center" size="1600,800" title="..:: Ciefpsettings Panel ::.. (Version{version})">
        <!-- Left 50% of the screen for the menu -->
        <widget name="menu" position="10,10" size="790,700" scrollbarMode="showOnDemand" itemHeight="50" font="Regular;26" />

        <!-- Right 50% of the screen for background image and buttons -->
        <widget name="background" position="800,0" size="800,800" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpsettingsPanel/background.png" zPosition="-1" alphatest="on" />

        <!-- Status at the bottom left -->
        <widget name="status" position="10,720" size="790,30" transparent="1" font="Regular;22" halign="center" />

        <!-- Yellow button below the status message on the left -->
        <widget name="key_yellow" position="10,760" size="400,40" font="Bold;22" halign="center" backgroundColor="#9F9F13" foregroundColor="#000000" />

        <!-- Green button on the right side -->
        <widget name="key_green" position="400,760" size="400,40" font="Bold;22" halign="center" backgroundColor="#1F771F" foregroundColor="#000000" />

        <!-- Red button on the right side -->
        <widget name="key_red" position="800,760" size="400,40" font="Bold;22" halign="center" backgroundColor="#9F1313" foregroundColor="#000000" />

        <!-- Blue button on the right side -->
        <widget name="key_blue" position="1200,760" size="400,40" font="Bold;22" halign="center" backgroundColor="#13389F" foregroundColor="#000000" />
    </screen>
    """.format(version=PLUGIN_VERSION)

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        self.selected_plugins = set()
        self.plugin_display_list = [f"[ ] {plugin}" for plugin in PLUGINS.keys()]
        self.current_install_index = 0
        self.installed_plugins = set()  # Privremena lista za praćenje uspešno instaliranih plugina
        self.version_check_in_progress = False
        self.version_buffer = b''

        self["menu"] = MenuList(self.plugin_display_list)
        self["background"] = Pixmap()
        self["status"] = Label("Select plugins with OK, install with Green")
        self["key_red"] = Button("Red: Plugin Manager")
        self["key_green"] = Button("Green: Install Selected")
        self["key_blue"] = Button("Blue: Restart Enigma2")
        self["key_yellow"] = Button("Yellow: IPK/TAR.GZ Installer")

        self["actions"] = ActionMap(
            ["ColorActions", "SetupActions"],
            {
                "red": self.open_plugin_manager,
                "green": self.start_installation,
                "ok": self.toggle_selection,
                "blue": self.restart_enigma2,
                "yellow": self.open_ipk_installer,
                "cancel": self.close,
            },
        )

        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.command_finished)
        self.update_status()

        # Automatska provera verzije pri pokretanju
        self.check_version_timer = eTimer()
        self.check_version_timer.callback.append(self.check_for_updates)
        self.check_version_timer.start(1000, True)  # Pokreni proveru nakon 1 sekunde

    def toggle_selection(self):
        """Toggle selection of the current plugin and log it immediately."""
        current_index = self["menu"].getSelectionIndex()
        current_plugin = list(PLUGINS.keys())[current_index]

        if current_plugin in self.selected_plugins:
            self.selected_plugins.remove(current_plugin)
            self.plugin_display_list[current_index] = f"[ ] {current_plugin}"
            # Ukloni plugin iz txt fajla ako je deselektovan
            self.remove_plugin_from_file(current_plugin)
        else:
            self.selected_plugins.add(current_plugin)
            self.plugin_display_list[current_index] = f"[X] {current_plugin}"
            # Upis plugin u txt fajl odmah nakon selekcije
            self.log_selected_plugin(current_plugin)

        self["menu"].setList(self.plugin_display_list)
        self.update_status()

    def update_status(self):
        """Update status bar with number of selected items."""
        count = len(self.selected_plugins)
        if count == 0:
            self["status"].setText("Select plugins with OK, install with Green")
        elif count == 1:
            self["status"].setText("1 item selected")
        else:
            self["status"].setText(f"{count} items selected")

    def log_selected_plugin(self, plugin):
        """Log a single selected plugin to the file, avoiding duplicates."""
        try:
            logging.debug(f"Logging selected plugin: {plugin}")
            # Proveri da li direktorijum postoji, ako ne, kreiraj ga
            plugin_dir = os.path.dirname(INSTALLED_PLUGINS_FILE)
            if not os.path.exists(plugin_dir):
                os.makedirs(plugin_dir)
                logging.debug(f"Created directory: {plugin_dir}")

            # Učitaj postojeće plugine iz fajla
            existing_plugins = set()
            if os.path.exists(INSTALLED_PLUGINS_FILE):
                with open(INSTALLED_PLUGINS_FILE, "r") as f:
                    existing_plugins = {line.strip() for line in f if line.strip()}
                logging.debug(f"Existing plugins in file: {existing_plugins}")

            # Ako plugin već postoji, preskoči
            if plugin not in existing_plugins:
                with open(INSTALLED_PLUGINS_FILE, "a") as f:
                    f.write(f"{plugin}\n")
                logging.debug(f"Successfully logged plugin {plugin} to {INSTALLED_PLUGINS_FILE}")
            else:
                logging.debug(f"Plugin {plugin} already exists in {INSTALLED_PLUGINS_FILE}")

        except Exception as e:
            logging.error(f"Error logging plugin {plugin} to {INSTALLED_PLUGINS_FILE}: {str(e)}")
            self["status"].setText(f"Error logging plugin {plugin}: {str(e)}")

    def remove_plugin_from_file(self, plugin):
        """Uklanja plugin iz txt fajla ako je deselektovan ili instalacija nije uspela."""
        try:
            if os.path.exists(INSTALLED_PLUGINS_FILE):
                with open(INSTALLED_PLUGINS_FILE, "r") as f:
                    plugins = [line.strip() for line in f if line.strip()]
                plugins = [p for p in plugins if p != plugin]
                with open(INSTALLED_PLUGINS_FILE, "w") as f:
                    for p in plugins:
                        f.write(f"{p}\n")
                logging.debug(f"Removed plugin {plugin} from {INSTALLED_PLUGINS_FILE}")
        except Exception as e:
            logging.error(f"Error removing plugin {plugin} from {INSTALLED_PLUGINS_FILE}: {str(e)}")
            self["status"].setText(f"Error removing plugin {plugin}: {str(e)}")

    def find_plugin_folder(self, plugin_name):
        """Pronalazi folder plugina u Extensions direktorijumu, uzimajući u obzir sličnosti."""
        if not os.path.exists(EXTENSIONS_DIR):
            return None

        # Eksplicitna mapa naziva plugina i foldera
        PLUGIN_FOLDER_MAP = {
            "Levi45 Addons Manager": "Levi45Addons",  # Potvrđen tačan naziv foldera
            "TV Addon": "tvaddon",
            "SubsSupport 1.7.0-r18 Mnasr": "SubsSupport",
        }
        if plugin_name in PLUGIN_FOLDER_MAP:
            folder = PLUGIN_FOLDER_MAP[plugin_name]
            if os.path.exists(os.path.join(EXTENSIONS_DIR, folder)):
                return folder

        # Normalizacija naziva plugina
        normalized_name = re.sub(r'[\s\-\_]', '', plugin_name.lower())
        normalized_name = re.sub(r'\d+\.\d+\.\d+.*|r\d+', '', normalized_name)
        for folder in os.listdir(EXTENSIONS_DIR):
            normalized_folder = re.sub(r'[\s\-\_]', '', folder.lower())
            if normalized_folder == normalized_name or folder.lower() == plugin_name.lower():
                return folder
        return None

    def start_installation(self):
        """Start installing selected plugins one by one."""
        if not self.selected_plugins:
            self["status"].setText("No plugins selected!")
            return

        self.plugins_to_install = list(self.selected_plugins)
        self.current_install_index = 0
        self.installed_plugins.clear()  # Resetuj listu instaliranih plugina
        self.install_next_plugin()

    def install_next_plugin(self):
        """Install the next plugin in the queue."""
        logging.debug(f"Installing plugin {self.current_install_index + 1}/{len(self.plugins_to_install)}")
        if self.current_install_index >= len(self.plugins_to_install):
            self["status"].setText("All installations complete!")
            logging.debug(f"All installations complete, installed_plugins: {self.installed_plugins}")
            self.clear_selections()
            return

        plugin = self.plugins_to_install[self.current_install_index]
        self["status"].setText(f"Installing {plugin} ({self.current_install_index + 1}/{len(self.plugins_to_install)})...")
        logging.debug(f"Executing command for plugin: {plugin}")
        self.container.execute(PLUGINS[plugin])

    def command_finished(self, retval):
        """Handle completion of a plugin installation."""
        current_plugin = self.plugins_to_install[self.current_install_index]
        logging.debug(f"Installation finished for plugin {current_plugin}, return value: {retval}")
        folder_name = self.find_plugin_folder(current_plugin)
        package_installed = False

        # Provera da li je paket instaliran (za opkg ili dpkg)
        if folder_name:
            if os.system(f"opkg list-installed | grep -q enigma2-plugin-extensions-{folder_name.lower()}") == 0:
                package_installed = True
            elif os.system(f"dpkg -l | grep -q enigma2-plugin-extensions-{folder_name.lower()}") == 0:
                package_installed = True

        if retval == 0 and (folder_name or package_installed):
            logging.debug(f"Plugin {current_plugin} successfully installed in folder {folder_name or 'unknown'}")
            self.installed_plugins.add(current_plugin)
            self.current_install_index += 1
            self.install_next_plugin()
        else:
            logging.warning(f"Plugin {current_plugin} not found in {EXTENSIONS_DIR} or not installed, retval: {retval}")
            self["status"].setText(f"Plugin {current_plugin} not installed properly!")
            self.remove_plugin_from_file(current_plugin)
            self.current_install_index += 1
            self.install_next_plugin()

    def clear_selections(self):
        """Clear selections and reset display."""
        self.selected_plugins.clear()
        self.plugin_display_list = [f"[ ] {plugin}" for plugin in PLUGINS.keys()]
        self["menu"].setList(self.plugin_display_list)
        self.update_status()

    def open_plugin_manager(self):
        """Open the Plugin Manager screen."""
        self.session.open(CiefpPluginManager)

    def open_ipk_installer(self):
        """Open the IPK/TAR.GZ Installer screen if files are available."""
        ipk_files = glob.glob("/tmp/*.ipk")
        tar_gz_files = glob.glob("/tmp/*.tar.gz")
        if not (ipk_files or tar_gz_files):
            self["status"].setText("There are no IPK or TAR.GZ files available in /tmp")
            logging.debug("No IPK or TAR.GZ files found in /tmp, skipping IPKInstaller screen")
            return
        self.session.open(IPKInstaller)

    def check_for_updates(self):
        """Provera dostupnih ažuriranja."""
        try:
            if self.version_check_in_progress:
                return
            self.version_check_in_progress = True
            self["status"].setText("Checking for updates...")
            self.version_buffer = b''
            self.container = eConsoleAppContainer()
            self.container.dataAvail.append(self.version_data_avail)
            self.container.appClosed.append(self.version_check_closed)
            self.container.execute(f"wget -q -O - {VERSION_URL}")
        except Exception as e:
            self.version_check_in_progress = False
            self["status"].setText(f"Update error: {str(e)}")
            logging.error(f"Error checking for updates: {str(e)}")

    def version_data_avail(self, data):
        """Sakupljanje podataka o verziji."""
        self.version_buffer += data

    def version_check_closed(self, retval):
        """Obrada rezultata provere verzije."""
        self.version_check_in_progress = False
        if retval == 0:
            try:
                remote_version = self.version_buffer.decode().strip()
                if remote_version != PLUGIN_VERSION:
                    self.session.openWithCallback(
                        self.start_update,
                        MessageBox,
                        f"Update available ({remote_version}). Install now?",
                        MessageBox.TYPE_YESNO
                    )
                else:
                    self["status"].setText("Plugin is up to date.")
            except Exception as e:
                self["status"].setText(f"Update check failed: {str(e)}")
                logging.error(f"Error decoding version data: {str(e)}")
        else:
            self["status"].setText("Update check failed.")
            logging.error(f"Version check failed with return value: {retval}")

    def start_update(self, answer):
        """Pokretanje ažuriranja ako je korisnik potvrdio."""
        if answer:
            try:
                self["status"].setText("Backing up installed plugins list...")
                # Provera da li fajl postoji i pravljenje backup-a
                if os.path.exists(INSTALLED_PLUGINS_FILE):
                    shutil.copy2(INSTALLED_PLUGINS_FILE, BACKUP_PLUGINS_FILE)
                    logging.debug(f"Backed up {INSTALLED_PLUGINS_FILE} to {BACKUP_PLUGINS_FILE}")
                else:
                    logging.debug(f"No {INSTALLED_PLUGINS_FILE} found for backup")

                self["status"].setText("Updating plugin...")
                self.container = eConsoleAppContainer()
                self.container.appClosed.append(self.update_completed)
                self.container.execute(UPDATE_COMMAND)
            except Exception as e:
                self["status"].setText(f"Backup error: {str(e)}")
                logging.error(f"Error during backup: {str(e)}")

    def update_completed(self, retval):
        """Obrada završetka ažuriranja."""
        try:
            # Pokušaj vraćanja backup fajla
            if os.path.exists(BACKUP_PLUGINS_FILE):
                # Proveri da li direktorijum postoji, ako ne, kreiraj ga
                plugin_dir = os.path.dirname(INSTALLED_PLUGINS_FILE)
                if not os.path.exists(plugin_dir):
                    os.makedirs(plugin_dir)
                    logging.debug(f"Created directory: {plugin_dir}")

                shutil.move(BACKUP_PLUGINS_FILE, INSTALLED_PLUGINS_FILE)
                logging.debug(f"Restored {BACKUP_PLUGINS_FILE} to {INSTALLED_PLUGINS_FILE}")
            else:
                logging.debug(f"No backup file {BACKUP_PLUGINS_FILE} found for restoration")

            if retval == 0:
                self["status"].setText("Update successful. Restarting...")
                self.session.open(TryQuitMainloop, 3)
            else:
                self["status"].setText("Update failed.")
                logging.error(f"Update failed with return value: {retval}")
        except Exception as e:
            self["status"].setText(f"Restore error: {str(e)}")
            logging.error(f"Error during restore: {str(e)}")

    def restart_enigma2(self):
        """Restart Enigma2."""
        self.container.execute("init 4 && init 3")
        self.close()

def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="Ciefpsettings Panel",
            description=f"Manage and install plugins (Version {PLUGIN_VERSION})",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon="icon.png",
            fnc=lambda session, **kwargs: session.open(CiefpsettingsPanel),
        )
    ]