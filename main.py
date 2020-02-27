from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys

class myListWidget(QListWidget):

   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You installed: "+item.text())
		
def main():
    #flashSplash()
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap('images/hi.png'))
    splash.show()
    QTimer.singleShot(2000, splash.close)
    
    listWidget = myListWidget()
	
   #Resize width and height
    listWidget.resize(600,700)
    listWidget.addItem("lucky block"); 
    listWidget.addItem("twilight forest");
    listWidget.addItem("Iron Chests Mod");
    listWidget.addItem("Not Enough Items");
	
    listWidget.setWindowTitle('Adelphi')
    listWidget.itemClicked.connect(listWidget.Clicked)
   
    listWidget.show()
    sys.exit(app.exec_())
	

if __name__ == '__main__':
    main()