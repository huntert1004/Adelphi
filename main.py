from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

import json
import urllib.request
import sys


class myListWidget(QListWidget):
    def loadIcon(url):
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        icon = QIcon(pixmap)
        return icon
        
def main():
    #flashSplash()
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap('view/images/hi.png'))
    splash.show()
    QTimer.singleShot(2000, splash.close)
    sys.exit(app.exec_())
	

if __name__ == '__main__':
    main()