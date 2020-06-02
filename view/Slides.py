from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import urllib.request
"""dont use"""
class Slides(QWidget):
    def __init__(self, image_files, parent=None):
        QWidget.__init__(self, parent)
        print(image_files)
        self.image_files = image_files
        self.label = QLabel("", self)
        self.label.setGeometry(50, 150, 450, 350)

        #button
        self.button = QPushButton(". . .", self)
        self.button.setGeometry(200, 100, 140, 30)
        self.button.clicked.connect(self.timerEvent)
        self.timer = QBasicTimer()
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
        print(file)
        image = QPixmap()
        image.loadFromData(urllib.request.urlopen(file).read())
        self.label.setPixmap(image)
        self.setWindowTitle("{} --> {}".format(str(self.step), file))
        self.step += 1