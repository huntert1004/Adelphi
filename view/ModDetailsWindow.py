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

class ModDetailsWindow(QDialog):
    def __init__(self, parent):
      super(ModDetailsWindow, self).__init__(parent)

    def isForgeInstalled(self, modCompat):
        if os.name == 'nt':
            appData = os.getenv('APPDATA')
            test_directory = appData + "\\.minecraft\\versions"
        else:
            appData = str(Path.home())
            test_directory = appData + "/.minecraft/versions"

        modVersions = [x.strip() for x in modCompat.split(',')]
        for child in os.listdir(test_directory):
            for modVersion in modVersions:
                if (child.startswith(modVersion + "-forge")):
                    test_path = os.path.join(test_directory, child)
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
            self.installButton = QPushButton("Install Now")
            self.installButton.clicked.connect(lambda: self.install(mod.modfile))
            self.layout.addWidget(self.installButton)
        else:
            self.missingForgeLabel = QLabel("Please create a MinecraftForge installation of version " + mod.compat + " to install this mod.")
            self.layout.addWidget(self.missingForgeLabel)
        
        self.setLayout(self.layout)
    
    def install(self, modUrl):
        filename = modUrl.split("/")[-1]
        if os.name == 'nt':
            appData = os.getenv('APPDATA')
            mod_directory = appData + "\\.minecraft\\mods\\"
        else:
            appData = str(Path.home())
            mod_directory = appData + "/.minecraft/mods/"

        file = open(mod_directory +filename,"wb")
        #load data into file object
        with urllib.request.urlopen("https://minifymods.com" + modUrl) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)

        QMessageBox.information(self, "The Oasiis", "Install Successful")
        