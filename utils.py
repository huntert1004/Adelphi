from PyQt5
 import QtCore, QtGui
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class MainWindow(QtGui.QMainWindow):
                #(self,  parent=None) <- original code
    def __init__(self, image_files, parent=None):
        QtGui.QMainWindow.__init__(self,  parent)
        self.setupUi(self)

        #Initialized Widget here
        self.slides_widget = Slides(self)
        self.setCentralWidget(self.slides_widget)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1012, 532)

        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(470, 130, 451, 301))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))



class Slides(QtGui.QWidget):
    def __init__(self, image_files, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.image_files = image_files
        self.label = QtGui.QLabel("", self)
        self.label.setGeometry(50, 150, 450, 350)

        #button
        self.button = QtGui.QPushButton(". . .", self)
        self.button.setGeometry(200, 100, 140, 30)
        self.button.clicked.connect(self.timerEvent)
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.delay = 3000 #ms
        sTitle = "DIT Erasmus Page : {} seconds"
        self.setWindowTitle(sTitle.format(self.delay/1000.0))


    def timerEvent(self, e=None):
        if self.step >= len(self.image_files):
            self.timer.start(self.delay, self)
            self.step = 0
            return
        self.timer.start(self.delay, self)
        file = self.image_files[self.step]
        image = QPixmap(file)
        self.label.setPixmap(image)
        self.setWindowTitle("{} --> {}".format(str(self.step), file))
        self.step += 1

image_files = ["slide1.jpg", "slide2.jpg", "slide3.jpg", "slide4.jpg"]


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Form = MainWindow(image_files)
    ui = MainWindow(image_files)
    Form.show()
    sys.exit(app.exec_())