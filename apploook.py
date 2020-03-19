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


class myListWidget(QListWidget):

   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You installed: "+item.text())

class myLabelWidget(QLabel):
    title = ''
    image = ''
    description = ''
    compat = ''
    modfile = ''
        
    @pyqtSlot(QLabel)
    def Clicked(self,event):
        #print(event)
        modDetail = ModDetailsWindow(self, self)
        modDetail.setGeometry(100, 200, 100, 100)
        modDetail.setModal(True)
        #modDetail.show()
        mw = qtmodern.windows.ModernWindow(modDetail)
        mw.show()
        #QMessageBox.information(self, "Whatever", self.title)

class ModDetailsWindow(QDialog):
    
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
        layout = QVBoxLayout()
        imageLabel = QLabel()
        imageLabel.setPixmap(mod.image)
        layout.addWidget(imageLabel)
        layout.addWidget(QLabel(mod.title))
        layout.addWidget(QLabel(mod.description))
        layout.addWidget(QLabel("Minecraft Compatability: " + mod.compat))
        if (self.isForgeInstalled(mod.compat)):
            installButton = QPushButton("Install Now")
            installButton.clicked.connect(lambda: self.install(mod.modfile))
            layout.addWidget(installButton)
        else:
            missingForgeLabel = QLabel("Please create a MinecraftForge installation of version " + mod.compat + " to install this mod.")
            layout.addWidget(missingForgeLabel)
        
        self.setLayout(layout)
    
    def install(self, modUrl):
        #check if there is a compatible forge installation
        
        
        filename = modUrl.split("/")[-1]
        #filedata = urllib.request.urlretrieve("https://minifymods.com" + modUrl).read()
        file = open(os.getenv('APPDATA') + "\\.minecraft\\mods\\"+filename,"wb")
        #load data into file object
        with urllib.request.urlopen("https://minifymods.com" + modUrl) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)

        QMessageBox.information(self, "Adellphi", "Install Successful")
        
class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = 'The Oasiis'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 900
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        #self.show()
        
        mw = qtmodern.windows.ModernWindow(self)
        mw.show()
class MyTableWidget(QWidget):
           
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QScrollArea()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        self.tab1.setWidgetResizable(True)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        grid = QGridLayout()
        listWidget = myListWidget()
        #get data
        json_url = "https://minifymods.com/api/mods?_format=json"
        data = urllib.request.urlopen(json_url).read().decode()
        mods = json.loads(data);
        #gridmods = mods[:9]
        #listmods = mods[9:len(mods)]


        positions = [(i,j) for i in range(5) for j in range(4)]
                
        for position,item in zip(positions,mods):
            imageUrl = "https://minifymods.com" + item['field_screenshots']
            image = QPixmap()
            image.loadFromData(urllib.request.urlopen(imageUrl).read())
            imageLabel = myLabelWidget()
            
            imageLabel.title = item['title']
            imageLabel.description = item['body']
            imageLabel.compat = item['field_minecraft_compatibility']
            imageLabel.modfile = item['field_mod_file']
            imageLabel.image = image           
            imageLabel.setPixmap(image.scaled(300, 200, Qt.KeepAspectRatio))
            imageLabel.setFixedSize(300, 200)
            imageLabel.mousePressEvent = imageLabel.Clicked
            
            grid.addWidget(imageLabel, *position)
        
        #TODO loop over listmods and add to an instance of myListWidget

            #possibly do this
            grid.addWidget(listWidget)


        self.tab1.layout.addLayout(grid)
        self.tab1.setLayout(self.tab1.layout)
        #add grid to tab1
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    
    ex = App()
    sys.exit(app.exec_())
    
 
    