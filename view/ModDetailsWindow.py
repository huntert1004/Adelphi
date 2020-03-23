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
        print(mod_directory)
        if os.path.isdir(mod_directory):
            test_filepath = os.path.join(mod_directory,filename)
            print(test_filepath)
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
                self.uninstallButton = QPushButton("Uninstall Now")
                self.uninstallButton.clicked.connect(lambda: self.uninstall(mod.modfile))
                self.layout.addWidget(self.uninstallButton)
            else:
                self.installButton = QPushButton("Install Now")
                self.installButton.clicked.connect(lambda: self.install(mod.modfile))
                self.layout.addWidget(self.installButton)
        else:
            self.missingForgeLabel = QLabel("Please create a MinecraftForge installation of version " + mod.compat + " to install this mod.")
            self.layout.addWidget(self.missingForgeLabel)
        
        self.setLayout(self.layout)
    
    def uninstall(self, modFile):
        filename = modFile.split("/")[-1]
        mod_directory = ModsController.getModDirectory()
        file = os.path.join(mod_directory,filename)
        os.remove(file)

        QMessageBox.information(self, "Adellphi", "Uninstall Successful")        

    def install(self, modUrl):
        filename = modUrl.split("/")[-1]
        mod_directory = ModsController.getModDirectory()

        file = open(mod_directory +filename,"wb")
        #load data into file object
        with urllib.request.urlopen("https://minifymods.com" + modUrl) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)

        QMessageBox.information(self, "Adellphi", "Install Successful")
        