from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os
import shutil
import urllib.request
import qtmodern.styles
import qtmodern.windows
from view.MainWindow import MainWindow
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Adellphi'
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
class Ui_Dialog(object):
    def setupUi(self, Dialog):  
            Dialog.setObjectName("Dialog")  
            Dialog.resize(812, 632)  
            Dialog.setStyleSheet("background-color: rgb(0, 170, 255);")  
            self.frame = QtWidgets.QFrame(Dialog)  
            self.frame.setGeometry(QtCore.QRect(90, 80, 631, 461))  
            self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")  
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)  
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)  
            self.frame.setObjectName("frame")  
            self.label = QtWidgets.QLabel(self.frame)  
            self.label.setGeometry(QtCore.QRect(230, 80, 171, 51))  
            font = QtGui.QFont()  
            font.setPointSize(16)  
            self.label.setFont(font)  
            self.label.setStyleSheet("color: rgb(o, 0, 0);")  
            self.label.setObjectName("label")  
            self.label_2 = QtWidgets.QLabel(self.frame)  
            self.label_2.setGeometry(QtCore.QRect(90, 190, 121, 31))  
            font = QtGui.QFont()  
            font.setPointSize(12)  
            self.label_2.setFont(font)  
            self.label_2.setObjectName("label_2")  
            self.label_3 = QtWidgets.QLabel(self.frame)  
            self.label_3.setGeometry(QtCore.QRect(90, 260, 121, 21))  
            font = QtGui.QFont()  
            font.setPointSize(12)  
            self.label_3.setFont(font)  
            self.label_3.setObjectName("label_3")  
            self.lineEdit = QtWidgets.QLineEdit(self.frame)  
            self.lineEdit.setGeometry(QtCore.QRect(260, 190, 231, 31))  
            self.lineEdit.setStyleSheet("background-color: rgb(209, 207, 255);")  
            self.lineEdit.setObjectName("lineEdit")  
            self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)  
            self.lineEdit_2.setGeometry(QtCore.QRect(260, 260, 231, 31))  
            self.lineEdit_2.setStyleSheet("background-color:#d1cfff;")  
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)  
            self.lineEdit_2.setObjectName("lineEdit_2")  
            self.pushButton = QtWidgets.QPushButton(self.frame)  
            self.pushButton.setGeometry(QtCore.QRect(350, 360, 161, 41))  
            font = QtGui.QFont()  
            font.setPointSize(14)  
            self.pushButton.setFont(font)  
            self.pushButton.setStyleSheet("background-color: rgb(0, 170, 0);")  
            self.pushButton.setObjectName("pushButton")  
            self.pushButton_2 = QtWidgets.QPushButton(self.frame)  
            self.pushButton_2.setGeometry(QtCore.QRect(220, 360, 101, 41))  
            self.pushButton_2.setStyleSheet("background-color:#ffff7f;")  
            self.pushButton_2.setObjectName("pushButton_2")  
    
            self.retranslateUi(Dialog)  
            QtCore.QMetaObject.connectSlotsByName(Dialog)  
  
    def retranslateUi(self, Dialog):  
        _translate = QtCore.QCoreApplication.translate  
        Dialog.setWindowTitle(_translate("Dialog", "Adellphi"))  
        self.label.setText(_translate("Dialog", "Adellphi"))  
        self.label_2.setText(_translate("Dialog", "User Name"))  
        self.label_3.setText(_translate("Dialog", "Password"))  
        self.pushButton.setText(_translate("Dialog", "Log in"))  
        self.pushButton_2.setText(_translate("Dialog", "Sign up"))  
        self.pushButton.clicked.connect(lambda: self.MainWindow)
if __name__ == '__main__':
    import sys 
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap('images/ss.png'))
    splash.show()
    QTimer.singleShot(2000, splash.close)
    qtmodern.styles.dark(app)
    Dialog = QtWidgets.QDialog()  
    ui = Ui_Dialog()  
    ui.setupUi(Dialog)  
    Dialog.show()  
    ex = App()
    sys.exit(app.exec_())
    
 
    