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
from view.MainWindow import MainWindow

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
        
        self.table_widget = MainWindow(self)
        self.setCentralWidget(self.table_widget)
        #self.show()
        
        mw = qtmodern.windows.ModernWindow(self)
        mw.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    
    ex = App()
    sys.exit(app.exec_())
    
 
    