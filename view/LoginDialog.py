import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qtmodern

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        loginLbl = QLabel('Login')
        passwordLbl = QLabel('Password')
        self.login = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        uklad = QGridLayout(self)
        uklad.addWidget(loginLbl, 0, 0)
        uklad.addWidget(self.login, 0, 1)
        uklad.addWidget(passwordLbl, 1, 0)
        uklad.addWidget(self.password, 1, 1)
        uklad.addWidget(self.buttons, 2, 0, 2, 0)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.setModal(True)
        self.setGeometry(100, 200, 1000, 1000)
        self.setWindowTitle('Login to Minecraft')

    def loginpassword(self):
        return (self.login.text().strip(),
                self.password.text().strip())

    @staticmethod
    def getLoginpassword(parent=None):
        dialog = LoginDialog(parent)
        dialog.login.setFocus()
        dialog.setGeometry(100, 200, 100, 100)
        ok = dialog.exec_()
        #mw = qtmodern.windows.ModernWindow(dialog)
        #ok = mw.exec_()
        login, password = dialog.loginpassword()
        return (login, password, ok == QDialog.Accepted)