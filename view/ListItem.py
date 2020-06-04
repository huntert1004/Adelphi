from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ListItem(QListWidget):
      """list what you downloaded"""

   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You installed: "+item.text())

