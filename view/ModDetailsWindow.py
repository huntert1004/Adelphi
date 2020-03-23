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

    def isForgeInstalled(self, modCompat):
        versions_directory = ModsController.getVersionsDirectory()

        modVersions = [x.strip() for x in modCompat.split(',')]
        for child in os.listdir(versions_directory):
            for modVersion in modVersions:
                if (child.startswith(modVersion + "-forge")):
                    test_path = os.path.join(versions_directory, child)
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
        self.layout.addWidget(QLabel(mod.description))
        self.layout.addWidget(QLabel("Minecraft Compatability: " + mod.compat))
        if (self.isForgeInstalled(mod.compat)):

            if (self.isModInstalled(mod.modfile)):
                self.addUninstallButton(mod.modfile)
            else:
                self.addInstallButton(mod.modfile)
        else:
            self.missingForgeLabel = QLabel("Please create a MinecraftForge installation of version " + mod.compat + " to install this mod.")
            self.layout.addWidget(self.missingForgeLabel)
        
        self.setLayout(self.layout)

    def addUninstallButton(self, modfile):
        self.uninstallButton = QPushButton("Uninstall Now")
        self.uninstallButton.clicked.connect(lambda: self.uninstall(modfile))
        self.layout.addWidget(self.uninstallButton)

    def addInstallButton(self, modfile):
        self.installButton = QPushButton("Install Now")
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
        