from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from view.ModDetailsWindow import ModDetailsWindow
from view.ModImageWidget import ModImageWidget

from model.Mod import Mod

class GridItem(QWidget):
    mod = None     
    
    def __init__(self, parent):
      super().__init__()
      self.parent = parent
      self.mod = Mod()
      self.setFixedSize(300, 250)
    """defines grid"""
    def create(self, parent):      
      self.layout = QVBoxLayout()
      self.imageLabel = ModImageWidget(self.mod)
      self.imageLabel.mousePressEvent = self.clicked      
      self.layout.addWidget(self.imageLabel)
      self.textLabel = QLabel(self.mod.title)
      self.textLabel.mousePressEvent = self.clicked
      self.textLabel.setFixedSize(300, 20)
      self.layout.addWidget(self.textLabel)
      self.setLayout(self.layout)
"""creates grid"""
    @pyqtSlot(QLabel)
    def clicked(self,event):
      modDetail = ModDetailsWindow(self.mod)
      self.parent.tabs.addTab(modDetail,self.mod.title)    
      self.parent.tabs.setCurrentIndex(self.parent.tabs.count()-1)
"""addes it to Qmainwindow"""