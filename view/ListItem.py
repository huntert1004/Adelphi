from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ListItem(QListWidget):

   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You installed: "+item.text())

