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
        installButton = QPushButton("Install Now")
        installButton.clicked.connect(lambda: self.install(mod.modfile))
        layout.addWidget(installButton)
        
        self.setLayout(layout)
    
    def install(self, modUrl):
        filename = modUrl.split("/")[-1]
        #filedata = urllib.request.urlretrieve("https://minifymods.com" + modUrl).read()
        file = open(os.getenv('APPDATA') + "\\.minecraft\\mods\\"+filename,"wb")
        #load data into file object
        with urllib.request.urlopen("https://minifymods.com" + modUrl) as response:
            with file as tmp_file:
                shutil.copyfileobj(response, tmp_file)

        QMessageBox.information(self, "Whatever", modUrl)
        
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
        self.tab1.layout = QGridLayout(self)

        #get data
        json_url = "https://minifymods.com/api/mods?_format=json"
        data = urllib.request.urlopen(json_url).read().decode()
        mods = json.loads(data);
        
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
            
            self.tab1.layout.addWidget(imageLabel, *position)
            
       
        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    
    ex = App()
    sys.exit(app.exec_())
    
 
    