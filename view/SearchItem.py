from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from view.ModDetailsWindow import ModDetailsWindow
from view.ModImageWidget import ModImageWidget

from model.Mod import Mod

class SearchItem(QWidget):
    mod = None     
    
    def __init__(self, parent):
      super().__init__()
      self.parent = parent
      self.mod = Mod()
      #self.setFixedSize(300, 250)
    """defines search item"""
    def create(self, parent):      

      #------------#
      self.layout = QHBoxLayout()
      self.layout.setAlignment(Qt.AlignLeft)

      
      self.imageLabel = ModImageWidget(self.mod)
      self.imageLabel.mousePressEvent = self.clicked
      self.layout.addWidget(self.imageLabel)

      self.textWidget = QWidget()
      self.textWidgetLayout = QVBoxLayout()
      
      self.titleLabel = QLabel(self.mod.title)
      self.titleLabel.setStyleSheet("font-weight: bold; font-size: 2em")
      self.textWidgetLayout.addWidget(self.titleLabel)
      self.textWidgetLayout.addWidget(QLabel(self.mod.description))

      self.textWidget.setLayout(self.textWidgetLayout)
      self.textWidget.mousePressEvent = self.clicked
      self.layout.addWidget(self.textWidget)
      
      self.setLayout(self.layout)
"""sets layout"""
    @pyqtSlot(QLabel)
    def clicked(self,event):
      modDetail = ModDetailsWindow(self.mod)
      self.parent.tabs.addTab(modDetail,self.mod.title)    
      self.parent.tabs.setCurrentIndex(self.parent.tabs.count()-1)
"""addeds it to Qmainwindow"""