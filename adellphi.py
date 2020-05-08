from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os
import sys
import shutil
import urllib.request
import qtmodern.styles
import qtmodern.windows
from view.MainWindow import MainWindow
import pathlib
import sys

root = pathlib.Path()
if getattr(sys, 'frozen', False):
    root = pathlib.Path(sys._MEIPASS)
    qtmodern.styles._STYLESHEET = root / 'qtmodern/style.qss'
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Adellphi'
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 900
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MainWindow(self)
        self.table_widget.show()


if __name__ == '__main__':
    import sys, time
    app = QApplication(sys.argv)
    splash_pix = QPixmap('C:\\Users\\hunte\\OneDrive\\Desktop\\Adelphi\\splashscreen.gif')
    #exe null pix map fix C:\\Users\\hunte\\OneDrive\\Desktop\\Adelphi\\
    splash = QSplashScreen(splash_pix)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    QTimer.singleShot(1000, splash.close)
    qtmodern.styles.light(app)
    ex = App()
    sys.exit(app.exec_())
    
 
    