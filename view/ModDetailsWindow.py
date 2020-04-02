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
#from library.pml.main import *

class ModDetailsWindow(QDialog):
    def __init__(self, parent):
      super(ModDetailsWindow, self).__init__(parent)

    def isModInstalled(self,modFile):
        mod_directory = ModsController.getModDirectory()
        filename = modFile.split("/")[-1]
        if os.path.isdir(mod_directory):
            test_filepath = os.path.join(mod_directory,filename)
            if os.path.isfile(test_filepath):
                return True
            
    def getForgeVersion(self,modCompat):
        versions_directory = ModsController.getVersionsDirectory()

        modVersions = [x.strip() for x in modCompat.split(',')]
        for child in os.listdir(versions_directory):
            for modVersion in modVersions:
                if (child.startswith(modVersion + "-forge")):
                    return child

    def isForgeInstalled(self, modCompat):
        forge_dir = self.getForgeVersion(modCompat)
        versions_directory = ModsController.getVersionsDirectory()
        test_path = os.path.join(versions_directory, forge_dir)
        if os.path.isdir(test_path):
            return True
            
    def __init__(self, mod, parent=None):
        super().__init__(parent)
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
        self.layout.addWidget(QLabel("Minecraft Compatability: " + mod.compat))
        

        if (self.isForgeInstalled(mod.compat)):

            if (self.isModInstalled(mod.modfile)):
                self.addUninstallButton(mod.modfile)
            else:
                self.addInstallButton(mod.modfile)
            self.runbutton(mod.compat)
        else:
            self.missingForgeLabel = QLabel("Please create a MinecraftForge installation of version " + mod.compat + " to install this mod.")
            self.missingForgeLabel.setWordWrap(True)
            self.layout.addWidget(self.missingForgeLabel)
            modVersions = [x.strip() for x in mod.compat.split(',')]
            self.forgeInstallButton = QPushButton("Install Forge v" + modVersions[0])
            self.forgeInstallButton.clicked.connect(lambda: self.installForge(modVersions[0], mod.modfile))
            self.layout.addWidget(self.forgeInstallButton)
        
        self.setLayout(self.layout)

    def installForge(self, version, modfile):
        forgeDownloadUrl = "";
 
        if (version == "1.15.2"):
            forgeDownloadUrl = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.15.2-31.1.0/forge-1.15.2-31.1.0-installer.jar"
        elif (version == "1.12.2"):
            forgeDownloadUrl = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.12.2-14.23.5.2768/forge-1.12.2-14.23.5.2768-installer.jar"
        elif (version == "1.8.9"):
            forgeDownloadUrl = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.8.9-11.15.1.1722/forge-1.8.9-11.15.1.1722-installer.jar"
        elif (version == "1.7.10"):
            forgeDownloadUrl = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/1.7.10-10.13.4.1558-1.7.10/forge-1.7.10-10.13.4.1558-1.7.10-installer.jar"
 
        filename = forgeDownloadUrl.split("/")[-1]
        install_directory = ModsController.getDotMinecraftDirectory()

        file = open(install_directory +filename,"wb")
        #load data into file object
        with urllib.request.urlopen(forgeDownloadUrl) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)
                subprocess.call(["java","-jar",install_directory + "/" + filename])
        self.addInstallButton(modfile)
        self.layout.removeWidget(self.forgeInstallButton)
        QMessageBox.information(self, "Adellphi", "Forge v" + version + " Install Successful")

    def runbutton (self, modcompat):
        self.runmc = QPushButton("Run")
        forge_version = self.getForgeVersion(modcompat)
        self.runmc.clicked.connect(lambda: runminecraft(forge_version))
        self.layout.addWidget(self.runmc)
    

                                                          
    def addUninstallButton(self, modfile):
        self.uninstallButton = QPushButton("Uninstall Mod")
        self.uninstallButton.clicked.connect(lambda: self.uninstall(modfile))
        self.layout.addWidget(self.uninstallButton)

    def addInstallButton(self, modfile):
        self.installButton = QPushButton("Install Mod")
        self.installButton.clicked.connect(lambda: self.install(modfile))
        self.layout.addWidget(self.installButton)

    def uninstall(self, modfile):
        filename = modfile.split("/")[-1]
        mod_directory = ModsController.getModDirectory()
        file = os.path.join(mod_directory,filename)
        os.remove(file)
        self.layout.removeWidget(self.uninstallButton)
        self.addInstallButton(modfile)
        QMessageBox.information(self, "Adellphi", "Uninstall Successful")        

    def install(self, modfile):
        filename = modfile.split("/")[-1]
        mod_directory = ModsController.getModDirectory()

        file = open(mod_directory +filename,"wb")
        #load data into file object
        with urllib.request.urlopen("https://minifymods.com" + modfile) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)
        self.layout.removeWidget(self.installButton)
        self.addUninstallButton(modfile)        
        QMessageBox.information(self, "Adellphi", "Install Successful")
        
  