from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Button import Button
from Components.Pixmap import Pixmap
from enigma import eConsoleAppContainer
import urllib.request
import json
import os

# Verzija plugina
PLUGIN_VERSION = "v2.4"

# GitHub API za proveru najnovije verzije
GITHUB_API_URL = "https://api.github.com/repos/ciefp/CiefpsettingsPanel/releases/latest"

# Komande za instalaciju raznih plugina
PLUGINS = {
    "CiefpSettingsDownloader": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsDownloader/main/installer.sh -O - | /bin/sh",
    "CiefpsettingsMotor": "wget https://raw.githubusercontent.com/ciefp/CiefpsettingsMotor/main/installer.sh -O - | /bin/sh",
    "CiefpSelectSatellite": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSelectSatellite/main/installer.sh -O - | /bin/sh",
    "CiefpE2Converter": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpE2Converter/main/installer.sh -O - | /bin/sh",
    "CiefpWhitelistStreamrelay": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpWhitelistStreamrelay/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsStreamrelay PY3": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsStreamrelay/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsStreamrelay PY2": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsStreamrelayPY2/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsT2miAbertis": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertis/main/installer.sh -O - | /bin/sh",
    "CiefpSettingsT2miAbertisOpenPLi": "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpSettingsT2miAbertisOpenPLi/main/installer.sh -O - | /bin/sh",
    "Ciefp-Panel mod Emil Nabil": "wget -q --no-check-certificate https://github.com/emilnabil/download-plugins/raw/refs/heads/main/Ciefp-Panel/Ciefp-Panel.sh -O - | /bin/sh",
    "ONEupdater": "wget https://raw.githubusercontent.com/Sat-Club/ONEupdaterE2/main/installer.sh -O - | /bin/sh",
    "TV Addon": "wget https://dreambox4u.com/emilnabil237/plugins/tvaddon/installer.sh -O - | /bin/sh",
    "OpenATV softcamfeed": "wget -O - -q http://updates.mynonpublic.com/oea/feed | bash",
    "OpenATV Develop feed": "wget -O - -q https://feeds2.mynonpublic.com/devel-feed | bash",
    "OpenMultiboot_1.3": "wget https://raw.githubusercontent.com/emil237/openmultiboot/main/installer.sh  -O - | /bin/sh",
    "AjPanel": "wget https://raw.githubusercontent.com/biko-73/AjPanel/main/installer.sh -O - | /bin/sh",
    "Linuxsat Panel": "wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/LinuxsatPanel/main/installer.sh -O - | /bin/sh",
    "KeyAdder": "wget -q --no-check-certificate https://raw.githubusercontent.com/fairbird/KeyAdder/main/installer.sh -O - |/bin/sh",
    "levi45-AddonsManager": "wget https://dreambox4u.com/emilnabil237/plugins/levi45-addonsmanager/installer.sh -O - | /bin/sh",
    "Levi45MulticamManager": "wget https://dreambox4u.com/emilnabil237/plugins/levi45multicammanager/installer.sh -O - | /bin/sh",
    "RaedQuickSignal": "wget https://raw.githubusercontent.com/fairbird/RaedQuickSignal/main/installer.sh -O - | /bin/sh",
    "SubsSupport_1.5.8-r9": "wget https://dreambox4u.com/emilnabil237/plugins/SubsSupport/installer1.sh -O - | /bin/sh", 
    "SubsSupport_2.1": "wget https://dreambox4u.com/emilnabil237/plugins/SubsSupport/subssupport_2.1.sh -O - | /bin/sh",
    "SubsSupport": "wget https://raw.githubusercontent.com/biko-73/SubsSupport/main/installer.sh -qO - | /bin/sh",
    "ChocholousekPicons": "https://github.com/s3n0/e2plugins/raw/master/ChocholousekPicons/online-setup -qO - | bash -s install",
    "Multistalker Pro": "wget -q --no-check-certificate https://dreambox4u.com/emilnabil237/plugins/MultiStalkerPro/installer.sh -O - | /bin/sh",
    "The Weather": "wget https://raw.githubusercontent.com/biko-73/TheWeather/main/installer.sh -O - | /bin/sh",
    "Vavoo": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Vavoo_Stream/online-setup | bash",
    "Youtube": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/YouTube/installer.sh -qO - | /bin/sh",
    "vavoo_1.15": "wget https://dreambox4u.com/emilnabil237/plugins/vavoo/installer.sh -O - | /bin/sh", 
    "E2iPlayer": "wget --no-check-certificate https://gitlab.com/MOHAMED_OS/e2iplayer/-/raw/main/install-e2iplayer.sh?inline=false -qO - | /bin/sh",
    "XKlass": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/XKlass/online-setup | bash",
    "XCplugin": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/XC-Code/installer.sh -qO - | /bin/sh",
    "X-Streamity": "wget https://raw.githubusercontent.com/biko-73/xstreamity/main/installer.sh -qO - | /bin/sh",
    "JediMakerXtream": "wget https://raw.githubusercontent.com/biko-73/JediMakerXtream/main/installer.sh -qO - | /bin/sh",
    "HasBahCa": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/HasBahCa/installer.sh -qO - | /bin/sh",
    "PlutoTV": "wget https://raw.githubusercontent.com/MOHAMED19OS/Download/main/PlutoTV/installer.sh -qO - | /bin/sh",
    "SmartAddonsPanel": "wget https://raw.githubusercontent.com/emilnabil/download-plugins/refs/heads/main/SmartAddonspanel/smart-Panel.sh -O - | /bin/sh",
    "MagicPanel": "wget -q --no-check-certificate https://gitlab.com/h-ahmed/Panel/-/raw/main/MagicPanel-install.sh -O - | /bin/sh",
    "ElieSat Panel": "wget -q --no-check-certificate https://gitlab.com/eliesat/extensions/-/raw/main/ajpanel/eliesatpanel.sh -O - | /bin/sh",
    "Aj Panel custom menu": "wget https://raw.githubusercontent.com/biko-73/AjPanel/main/AJPanel_custom_menu_installer.sh -O - | /bin/sh",
    "Plugins by Emil Nabil": "wget --no-check-certificate -O library-plugins.sh https://raw.githubusercontent.com/emil237/download-plugins/main/library-plugins.sh && bash library-plugins.sh",
    "Oscam Mohamed_OS": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Cam_Emulator/online-setup | bash -s oscam ....... install OSCam Only\n",
    "Ncam Mohamed_OS": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Cam_Emulator/online-setup | bash -s ncam ..... install NCam Only\n",
    "Oscam Emu biko-73": "wget https://raw.githubusercontent.com/biko-73/OsCam_EMU/main/installer.sh -O - | /bin/sh",
    "Moviecam": "wget https://cutt.ly/Lw6Q9dsi --no-check-certificate -O - | /bin/sh",
    "Cccam": "wget https://dreambox4u.com/emilnabil237/emu/installer-cccam.sh  -O - | /bin/sh",
    "Stalker portal free": "wget -O /home/stalker.conf https://raw.githubusercontent.com/karimSATPRO/Portal-100mag/main/stalker.conf",
    "MADMAX IMPOSSIBLE SKIN OPENATV": "wget https://bit.ly/3cg1664 -qO - | /usr/bin/python",
    "BO-HLALA FHD SKIN": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerB.sh -O - | /bin/sh",
    "Metrix-FHD Skin": "wget http://ipkinstall.ath.cx/ipk-install/MetrixFHD/MetrixFHD.sh -qO - | /bin/sh",
    "Red-Dragon-FHD Skin": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerD.sh -O - | /bin/sh",
    "Nitro AdvanceFHD Skin": "wget https://raw.githubusercontent.com/biko-73/NitroAdvanceFHD/main/installer.sh -qO - | /bin/sh",
    "Desert skin": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerDs.sh -O - | /bin/sh",
    "XDREAMY skin": "wget -q --no-check-certificate https://raw.githubusercontent.com/Insprion80/Skins/main/xDreamy/installer.sh -O - | /bin/sh",
    "Al Ayam FHD skin": "wget https://raw.githubusercontent.com/biko-73/TeamNitro/main/script/installerAL.sh -O - | /bin/sh",
    "Aglare": "wget -qO- --no-check-certificate https://gitlab.com/MOHAMED_OS/dz_store/-/raw/main/Aglare/online-setup | bash",
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
    "feeds-finder": "wget -q --no-check-certificate https://dreambox4u.com/emilnabil237/plugins/feeds-finder/installer.sh -O - | /bin/sh",
    "Virtual Keyboard": "wget https://raw.githubusercontent.com/fairbird/NewVirtualKeyBoard/main/installer.sh -O - | /bin/sh",
    "OpenMultiboot_1.3": "wget https://raw.githubusercontent.com/emil237/openmultiboot/main/installer.sh  -O - | /bin/sh",
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

# Komanda za ažuriranje plugina
UPDATE_COMMAND = "wget -q --no-check-certificate https://raw.githubusercontent.com/ciefp/CiefpsettingsPanel/main/installer.sh -O - | /bin/sh"

class CiefpsettingsPanel(Screen):
    skin = """
    <screen name="CiefpsettingsPanel" position="center,center" size="1200,600" title="..:: Ciefpsettings Panel ::..">
        <!-- Left 50% of the screen for the menu -->
        <widget name="menu" position="10,10" size="600,500" scrollbarMode="showOnDemand" itemHeight="50" font="Regular;26" />

        <!-- Right 50% of the screen for background image and buttons -->
        <widget name="background" position="610,0" size="590,600" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CiefpsettingsPanel/background.png" zPosition="-1" alphatest="on" />

        <!-- Status at the bottom left -->
        <widget name="status" position="10,520" size="600,30" transparent="1" font="Regular;22" halign="center" />

        <!-- Red button on the right side -->
        <widget name="key_red" position="610,560" size="300,40" font="Bold;18" halign="center" backgroundColor="#9F1313" foregroundColor="#000000" />

        <!-- Green button on the right side -->
        <widget name="key_green" position="300,560" size="300,40" font="Bold;18" halign="center" backgroundColor="#1F771F" foregroundColor="#000000" />

        <!-- Blue button on the right side -->
        <widget name="key_blue" position="900,560" size="300,40" font="Bold;18" halign="center" backgroundColor="#13389F" foregroundColor="#000000" />

        <!-- Yellow button below the status message on the left -->
        <widget name="key_yellow" position="10,560" size="300,40" font="Bold;18" halign="center" backgroundColor="#9F9F13" foregroundColor="#000000" />
    </screen>
    """

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        self["menu"] = MenuList(list(PLUGINS.keys()))
        self["background"] = Pixmap()
        self["status"] = Label("Select a plugin to install")
        self["key_red"] = Button("Red: Exit")
        self["key_green"] = Button("Green/OK: Install")
        self["key_blue"] = Button("Blue: Restart Enigma2")
        self["key_yellow"] = Button("Yellow: Update Plugin")  # Novo žuto dugme

        self["actions"] = ActionMap(
            ["ColorActions", "SetupActions"],
            {
                "red": self.close,
                "green": self.install_plugin,
                "ok": self.install_plugin,
                "blue": self.restart_enigma2,
                "yellow": self.update_plugin,  # Dodana akcija za žuto dugme
                "cancel": self.close,
            },
        )

        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.command_finished)


    def prompt_update(self, answer):
        if answer:
            self.update_plugin()

    def update_plugin(self):
        """Metoda za ažuriranje plugina."""
        self["status"].setText("Updating plugin...")
        self.container.execute(UPDATE_COMMAND)

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
