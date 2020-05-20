import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os
import shutil
import urllib.request
import qtmodern.styles
import qtmodern.windows
from pathlib import Path
from controller.ModsController import ModsController
import subprocess
from library.pml.main import *
from view.LoginDialog import LoginDialog


class ModDetailsWindow(QDialog):
    def __init__(self, parent):
      super().__init__()

    def isModInstalled(self):
        
        mod_directory = ModsController.getModDirectory()
        filename = self.mod.modfile.split("/")[-1]
        if os.path.isdir(mod_directory):
            test_filepath = os.path.join(mod_directory,filename)
            if os.path.isfile(test_filepath):
                return True
            
    def getForgeVersion(self):
        try:
            versions_directory = ModsController.getVersionsDirectory()
            if (versions_directory):
                modVersions = [x.strip() for x in self.mod.compat.split(',')]
                for child in os.listdir(versions_directory):
                    for modVersion in modVersions:
                        if (child.lower().startswith(modVersion + "-forge")):
                            return child
        except:
            pass

    def isForgeInstalled(self):
        forge_dir = self.getForgeVersion()
        versions_directory = ModsController.getVersionsDirectory()

        if (versions_directory and forge_dir):
            test_path = os.path.join(versions_directory, forge_dir)
            if os.path.isdir(test_path):
                return True
            
    def __init__(self, mod, parent=None):
        super().__init__(parent)
        self.mod = mod
        self.name = mod.title
        self.setWindowTitle(mod.title)
        self.layout = QVBoxLayout()
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(mod.image)
        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(QLabel(mod.title))
        self.descriptionLabel = QLabel(mod.description)
        self.descriptionLabel.setWordWrap(True)
        self.layout.addWidget(self.descriptionLabel)
        self.layout.addWidget(QLabel("Minecraft Compatibility: " + mod.compat))
        

        if (self.isForgeInstalled()):

            if (self.isModInstalled()):
                self.addUninstallButton()                
            else:
                self.addInstallButton()

            self.addRunButton()
            self.addRunAsUserButton()
        else:
            self.missingForgeLabel = QLabel("Please create a MinecraftForge installation of version " + mod.compat + " to install this mod.")
            self.missingForgeLabel.setWordWrap(True)
            self.layout.addWidget(self.missingForgeLabel)
            modVersions = [x.strip() for x in mod.compat.split(',')]
            self.forgeInstallButton = QPushButton("Install Forge v" + modVersions[0])
            self.forgeInstallButton.clicked.connect(lambda: self.installForge(modVersions[0]))
            self.layout.addWidget(self.forgeInstallButton)
        
        self.setLayout(self.layout)

    def installForge(self, version):
        forgeDownloadUrl = "";
 
        if (version == "1.15.2"):
            forgeDownloadUrl = "https://minifymods.com/sites/default/files/forge-1.15.2-31.1.37-installer.jar"
        elif (version == "1.12.2"):
            forgeDownloadUrl = "https://minifymods.com/sites/default/files/forge-1.12.2-14.23.5.2813-installer.jar"
        elif (version == "1.8.9"):
            forgeDownloadUrl = "https://minifymods.com/sites/default/files/forge-1.8.9-11.15.1.1722-installer.jar"
        elif (version == "1.7.10"):
            forgeDownloadUrl = "https://minifymods.com/sites/default/files/forge-1.7.10-10.13.4.1558-1.7.10-installer.jar"
 
        filename = forgeDownloadUrl.split("/")[-1]
        install_directory = ModsController.getDotMinecraftDirectory()

        file = open(filename,"wb")
        #load data into file object
        with urllib.request.urlopen(forgeDownloadUrl) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)
                subprocess.call(["java","-jar", filename])
        self.addInstallButton()
        self.layout.removeWidget(self.forgeInstallButton)
        QMessageBox.information(self, "Adellphi", "Forge v" + version + " Install Successful")

    def addRunButton(self):
        self.runButton = QPushButton("Run with new login")
        forge_version = self.getForgeVersion()        
        self.runButton.clicked.connect(lambda: runminecraft(forge_version))
        self.layout.addWidget(self.runButton)

    def addRunAsUserButton(self):
        MAGIC_USERNAME_KEY = 'ADELLPHI_USERNAME'
        APP_ID = 'ADELLPHI'
        login = keyring.get_password(APP_ID, MAGIC_USERNAME_KEY)
        if (login):
            self.runAsUserButton = QPushButton("Run as " + login)
            forge_version = self.getForgeVersion()        
            self.runAsUserButton.clicked.connect(lambda: runminecraft(forge_version))
            self.layout.addWidget(self.runAsUserButton)
             
    def addUninstallButton(self):
        self.uninstallButton = QPushButton("Uninstall Mod")
        self.uninstallButton.clicked.connect(lambda: self.uninstall())
        self.layout.addWidget(self.uninstallButton)

    def addInstallButton(self):
        self.installButton = QPushButton("Install Mod")
        self.installButton.clicked.connect(lambda: self.install())
        self.layout.addWidget(self.installButton)

    def uninstall(self):
        filename = self.mod.modfile.split("/")[-1]
        mod_directory = ModsController.getModDirectory()
        file = os.path.join(mod_directory,filename)
        os.remove(file)
        self.layout.removeWidget(self.uninstallButton)
        self.addInstallButton()        
        QMessageBox.information(self, "Adellphi", "Uninstall Successful")        

    def install(self):
        filename = self.mod.modfile.split("/")[-1]
        mod_directory = ModsController.getModDirectory()

        file = open(mod_directory +filename,"wb")
        #load data into file object
        with urllib.request.urlopen("https://minifymods.com" + self.mod.modfile) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        self.layout.removeWidget(self.installButton)
        self.addUninstallButton()   
        QMessageBox.information(self, "Adellphi", "Install Successful")
        
  