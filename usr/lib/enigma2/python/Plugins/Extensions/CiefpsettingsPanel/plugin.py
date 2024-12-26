from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Button import Button
from enigma import eConsoleAppContainer
import urllib.request
import json

# Verzija plugina
PLUGIN_VERSION = "1.3"

# GitHub API za proveru najnovije verzije
GITHUB_API_URL = "https://api.github.com/repos/ciefp/CiefpsettingsPanel/releases/latest"

# Komande za instalaciju raznih plugina
PLUGINS = {
    "CiefpSettingsDownloader": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsDownloader/main/installer.sh -O - | /bin/sh",
    "CiefpsettingsMotor": "wget https://raw.githubusercontent.com/ciefp/CiefpsettingsMotor/main/installer.sh -O - | /bin/sh",
    "CiefpWhitelistStreamrelay": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpWhitelistStreamrelay/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsT2miAbertis": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertis/main/installer.sh -O - | /bin/sh",
    "ONEupdater": "wget https://raw.githubusercontent.com/Sat-Club/ONEupdaterE2/main/installer.sh -O - | /bin/sh",
    "TV Addon": "wget https://dreambox4u.com/emilnabil237/plugins/tvaddon/installer.sh -O - | /bin/sh",
    "OpenATV softcamfeed": "wget -O - -q http://updates.mynonpublic.com/oea/feed | bash",
    "OpenATV Develop feed": "wget -O - -q https://feeds2.mynonpublic.com/devel-feed | bash",
    "AjPanel": "wget https://raw.githubusercontent.com/biko-73/AjPanel/main/installer.sh -O - | /bin/sh",
    "Linuxsat Panel": "wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/installer.sh -O - | /bin/sh",
    "KeyAdder": "wget -q --no-check-certificate https://raw.githubusercontent.com/fairbird/KeyAdder/main/installer.sh -O - |/bin/sh",
    "RaedQuickSignal": "wget https://raw.githubusercontent.com/fairbird/RaedQuickSignal/main/installer.sh -O - | /bin/sh",
    "SubsSupport": "wget https://raw.githubusercontent.com/biko-73/SubsSupport/main/installer.sh -qO - | /bin/sh",
    "ChocholousekPicons": "https://github.com/s3n0/e2plugins/raw/master/ChocholousekPicons/online-setup -qO - | bash -s install",
    "Multistalker Pro": "wget -q --no-check-certificate https://dreambox4u.com/emilnabil237/plugins/MultiStalkerPro/installer.sh -O - | /bin/sh",
    "The Weather": "wget https://raw.githubusercontent.com/biko-73/TheWeather/main/installer.sh -O - | /bin/sh",
    "Youtube": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/YouTube/installer.sh -qO - | /bin/sh",
    "E2iPlayer": "wget --no-check-certificate https://gitlab.com/MOHAMED_OS/e2iplayer/-/raw/main/install-e2iplayer.sh?inline=false -qO - | /bin/sh",
    "XCplugin": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/XC-Code/installer.sh -qO - | /bin/sh",
    "X-Streamity": "wget https://raw.githubusercontent.com/biko-73/xstreamity/main/installer.sh -qO - | /bin/sh",
    "JediMakerXtream": "wget https://raw.githubusercontent.com/biko-73/JediMakerXtream/main/installer.sh -qO - | /bin/sh",
    "HasBahCa": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/HasBahCa/installer.sh -qO - | /bin/sh",
    "PlutoTV": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/PlutoTV/installer.sh -qO - | /bin/sh",
    "ElieSat Panel": "wget -q --no-check-certificate https://gitlab.com/eliesat/extensions/-/raw/main/ajpanel/eliesatpanel.sh -O - | /bin/sh",
    "Aj Panel custom menu": "wget https://raw.githubusercontent.com/biko-73/AjPanel/main/AJPanel_custom_menu_installer.sh -O - | /bin/sh",
    "Plugins by Emil Nabil": "wget --no-check-certificate -O library-plugins.sh https://raw.githubusercontent.com/emil237/download-plugins/main/library-plugins.sh && bash library-plugins.sh",
    "Oscam Mohamed_OS": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Cam_Emulator/online-setup | bash -s oscam ....... install OSCam Only\n",
    "Ncam Mohamed_OS": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Cam_Emulator/online-setup | bash -s ncam ..... install NCam Only\n",
    "Oscam Emu biko-73": "wget https://raw.githubusercontent.com/biko-73/OsCam_EMU/main/installer.sh -O - | /bin/sh",
    "Moviecam": "wget https://cutt.ly/Lw6Q9dsi --no-check-certificate -O - | /bin/sh",
    "Stalker portal free": "wget -O /home/stalker.conf https://raw.githubusercontent.com/karimSATPRO/Portal-100mag/main/stalker.conf",
    "MADMAX IMPOSSIBLE SKIN OPENATV": "wget https://bit.ly/3cg1664 -qO - | /usr/bin/python",
    "BO-HLALA FHD SKIN": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerB.sh -O - | /bin/sh",
    "Metrix-FHD": "wget http://ipkinstall.ath.cx/ipk-install/MetrixFHD/MetrixFHD.sh -qO - | /bin/sh",
    "Red-Dragon-FHD": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerD.sh -O - | /bin/sh",
    "Nitro AdvanceFHD": "wget https://raw.githubusercontent.com/biko-73/NitroAdvanceFHD/main/installer.sh -qO - | /bin/sh",
    "Desert skin": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerDs.sh -O - | /bin/sh",
    "XDREAMY skin": "wget -q --no-check-certificate https://raw.githubusercontent.com/Insprion80/Skins/main/xDreamy/installer.sh -O - | /bin/sh",
    "XtraEvante": "wget https://github.com/digiteng/xtra/raw/main/xtraEvent.sh -qO - | /bin/sh",
    "E2iPlayer_TSIPlayer": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/E2IPLAYER_TSiplayer/installer.sh -qO - | /bin/sh",
    "FootOnsat": "wget https://raw.githubusercontent.com/ziko-ZR1/FootOnsat/main/Download/install.sh -qO - | /bin/sh",
    "FooTOnSat New": "wget --no-check-certificate https://raw.githubusercontent.com/MOHAMED19OS/Enigma2_Store/main/FootOnsat/installer.py -qO - | python",
    "FreeServerCCcam": "wget https://ia803104.us.archive.org/0/items/freecccamserver/installer.sh -qO - | /bin/sh",
    "feeds-finder": "wget -q --no-check-certificate https://dreambox4u.com/emilnabil237/plugins/feeds-finder/installer.sh -O - | /bin/sh",
    "ShootYourScreen-Py3": "wget -q --no-check-certificate https://raw.githubusercontent.com/emil237/ShootYourScreen-Py3/main/ShootYourScreen-py3.sh -O - | /bin/sh",
    "update": "opkg update",
    "astra-sm": "opkg install astra-sm",
    "reboot": "reboot",
    "restartEnigma2": "killall -9 enigma2",
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
    "Reboots Enigma2": "nit 6",
    "Deep Standby": "init 0",
}

class CiefpsettingsPanel(Screen):
    skin = """
    <screen name="CiefpsettingsPanel" position="center,center" size="900,600" title="Ciefpsettings Panel">
        <widget name="menu" position="10,10" size="880,500" scrollbarMode="showOnDemand" font="Regular;24" />
        <widget name="status" position="10,520" size="880,30" font="Regular;22" halign="center" />
        <widget name="key_red" position="10,560" size="200,40" font="Regular;18" halign="center" backgroundColor="#9F1313" />
        <widget name="key_green" position="350,560" size="200,40" font="Regular;18" halign="center" backgroundColor="#1F771F" />
        <widget name="key_blue" position="690,560" size="200,40" font="Regular;18" halign="center" backgroundColor="#13389F" />
    </screen>
    """

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        self["menu"] = MenuList(list(PLUGINS.keys()))
        self["status"] = Label("Select a plugin to install")
        self["key_red"] = Button("Red: Exit")
        self["key_green"] = Button("Green/OK: Install")
        self["key_blue"] = Button("Blue: Restart Enigma2")

        self["actions"] = ActionMap(
            ["ColorActions", "SetupActions"],
            {
                "red": self.close,
                "green": self.install_plugin,
                "ok": self.install_plugin,
                "blue": self.restart_enigma2,
                "cancel": self.close,
            },
        )

        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.command_finished)

        # Provera nove verzije pri otvaranju
        self.check_for_update()

    def check_for_update(self):
        try:
            response = urllib.request.urlopen(GITHUB_API_URL)
            data = json.load(response)
            latest_version = data["tag_name"].lstrip("v")  # Pretpostavka: verzije koriste 'v' prefix
            if latest_version > PLUGIN_VERSION:
                self["status"].setText(f"New version available: {latest_version}. Please update!")
            else:
                self["status"].setText("You are using the latest version.")
        except Exception as e:
            self["status"].setText(f"Error checking for updates: {e}")

    def install_plugin(self):
        selected = self["menu"].getCurrent()
        if selected:
            command = PLUGINS[selected]
            self["status"].setText(f"Installing {selected}...")
            self.container.execute(command)

    def command_finished(self, retval):
        self["status"].setText("Installation complete!" if retval == 0 else "Error during installation!")

    def restart_enigma2(self):
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
