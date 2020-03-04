from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

import json
import urllib.request
import sys


class myListWidget(QListWidget):

   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You installed: "+item.text())

def loadIcon(url):
    data = urllib.request.urlopen(url).read()
    pixmap = QPixmap()
    pixmap.loadFromData(data)
    icon = QIcon(pixmap)
    return icon
    
def main():
    #flashSplash()
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap('images/hi.png'))
    splash.show()
    QTimer.singleShot(2000, splash.close)
    
    listWidget = myListWidget()
	
   #Resize width and height
    listWidget.resize(600,700)
    #get data
    json_url = "https://minifymods.com/api/mods?_format=json"
    data = urllib.request.urlopen(json_url).read().decode()
    mods = json.loads(data);
    
    for item in mods:
        mod = QListWidgetItem()
        modWidget = QWidget()
        modWidgetText = QLabel(item['title'])
        modWidgetButton = QPushButton("Install")
        modWidgetLayout = QHBoxLayout()
        modWidgetLayout.addWidget(modWidgetText)
        modWidgetLayout.addWidget(modWidgetButton)
        modWidgetLayout.addStretch()

        modWidgetLayout.setSizeConstraint(QHBoxLayout.SetFixedSize)   
        modWidget.setLayout(modWidgetLayout)
        mod.setSizeHint(modWidget.sizeHint())
        image = item['field_screenshots']
        mod.setIcon(loadIcon("https://minifymods.com" + image))
        listWidget.addItem(mod)
        listWidget.setItemWidget(mod, modWidget)
        
    
    listWidget.setIconSize(QSize(128, 128))
    listWidget.setWindowTitle('Adelphi')
    listWidget.itemClicked.connect(listWidget.Clicked)
   
    listWidget.show()
    sys.exit(app.exec_())
	

if __name__ == '__main__':
    main()