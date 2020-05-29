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
import platform

root = pathlib.Path()
if getattr(sys, 'frozen', False):
    root = pathlib.Path(sys._MEIPASS)
    qtmodern.styles._STYLESHEET = root / 'qtmodern/style.qss' 
    #hidden imports in exe file
class TitleBar(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        css = """
        QWidget{
            Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            Background-image:url('adellphi.png');
            font-size:12px;
            color: black;

        }
        QToolButton{
            Background:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #FF00FF;
            font-size:11px;
        }
        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Highlight)
        self.setStyleSheet(css)
        self.minimize=QToolButton(self)
        self.minimize.setIcon(QIcon('img/min.png'))
        self.maximize=QToolButton(self)
        self.maximize.setIcon(QIcon('img/max.png'))
        close=QToolButton(self)
        close.setIcon(QIcon('img/close.png'))
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)
        label=QLabel(self)
        label.setText("Window Title")
        self.setWindowTitle("Window Title")
        hbox=QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.maxNormal=False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        box.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            box.showNormal()
            self.maxNormal= False
            self.maximize.setIcon(QIcon('img/max.png'))
            print('1')
        else:
            box.showMaximized()
            self.maxNormal=  True
            print('2')
            self.maximize.setIcon(QIcon('img/max2.png'))

    def close(self):
        box.close()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            box.moving = True
            box.offset = event.pos()

    def mouseMoveEvent(self,event):
        if box.moving: box.move(event.globalPos()-box.offset)


class App(QMainWindow):
    def __init__(self):
      super().__init__()
      self.title = 'Adellphi'
      self.titleBar = TitleBar(self)
      self.left = 0
      self.top = 0
      self.width = 1280
      self.height = 900
      self.setWindowTitle(self.title)
      self.setGeometry(self.left, self.top, self.width, self.height)
      self.table_widget = MainWindow(self)
      self.table_widget.show()
      self.setWindowFlags(Qt.FramelessWindowHint)
      


class Frame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.m_mouse_down= False
        self.setFrameShape(QFrame.StyledPanel)
        css = """
        QFrame{
            Background:  #D700D7;
            color:white;
            font:13px ;
            font-weight:bold;
            }
        """
        self.setStyleSheet(css)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar= TitleBar(self)
        self.m_content= MainWindow(self)
        vbox=QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        layout=QVBoxLayout()
        layout.addWidget(self.m_content)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        vbox.addLayout(layout)
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 900
        self.setGeometry(self.left, self.top, self.width, self.height)
        # Allows you to access the content area of the frame
        # where widgets and layouts can be added

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self,event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button()== Qt.LeftButton

    def mouseMoveEvent(self,event):
        x=event.x()
        y=event.y()

    def mouseReleaseEvent(self,event):
        m_mouse_down=False
#init the gmain windo widget sets the size and title

if __name__ == '__main__':
    import sys, time
    app = QApplication(sys.argv)
    imageroot = ""
    if platform.system() == 'Windows':
        splash_pix = QPixmap('C:\\Users\\hunte\\Desktop\\Adelphi\\splashscreen.gif')
        imageroot = 'C:\\Users\\hunte\\Desktop\\Adelphi'
    elif platform.system() == "Darwin":
        splash_pix = QPixmap('/Users/angiethomas/Desktop/Adelphi/splashscreen.gif')
        imageroot = '/Users/angiethomas/Desktop/Adelphi'
    #exe null pix map fix C:\\Users\\hunte\\OneDrive\\Desktop\\Adelphi\\
    splash = QSplashScreen(splash_pix)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    QTimer.singleShot(1000, splash.close)
    #qtmodern.styles.light(app)
    #ex = App()
    box = Frame()
    box.show()
    sys.exit(app.exec_())
    #runs adellphi
 
    