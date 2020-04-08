from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.ModDetailsWindow import ModDetailsWindow
import qtmodern
import urllib.request

class GridItem(QWidget):
    mod = None
    class Mod():
      title = ''
      imageUrl = ''
      description = ''
      compat = ''
      modfile = ''
      image = None
    
    
    
    def __init__(self, parent):
      super(GridItem, self).__init__(parent)
      self.parent = parent
      self.mod = self.Mod()
    
    def create(self, parent):
      
      self.layout = QVBoxLayout()
      
      self.imageLabel = QLabel()
      self.mod.image = QPixmap()
      self.mod.image.loadFromData(urllib.request.urlopen(self.mod.imageUrl).read())
      self.imageLabel.image = self.mod.image           
      self.imageLabel.setPixmap(self.mod.image.scaled(300, 200, Qt.KeepAspectRatio))
      self.imageLabel.setFixedSize(300, 200)
      self.imageLabel.mousePressEvent = self.clicked
      
      self.layout.addWidget(self.imageLabel)
      
      self.textLabel = QLabel(self.mod.title)
      self.textLabel.mousePressEvent = self.clicked
      self.layout.addWidget(self.textLabel)
      
      self.setLayout(self.layout)
     
    @pyqtSlot(QLabel)
    def clicked(self,event):
      #print(event)
      self.modDetail = ModDetailsWindow(self.mod)
      self.modDetail.setGeometry(100, 200, 100, 100)
      self.modDetail.setModal(True)
      #modDetail.show()
      mw = qtmodern.windows.ModernWindow(self.modDetail)
      mw.show()