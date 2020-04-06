from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.ModDetailsWindow import ModDetailsWindow
import qtmodern

class GridItem(QLabel):
    title = ''
    image = ''
    description = ''
    compat = ''
    modfile = ''
    
    
    
    def __init__(self, parent):
      super(GridItem, self).__init__(parent)
      self.parent = parent
     
    @pyqtSlot(QLabel)
    def Clicked(self,event):
      #print(event)
      self.modDetail = ModDetailsWindow(self)
      self.modDetail.setGeometry(100, 200, 100, 100)
      self.modDetail.setModal(True)
      #modDetail.show()
      mw = qtmodern.windows.ModernWindow(self.modDetail)
      mw.show()