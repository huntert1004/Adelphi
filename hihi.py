import sys
import os
import utils
from PyQt5 import *
from PyQt5.QtWidgets import *


class SlideShowPics(QSplashScreen):
 def _createSplashScreen(self):
        return QSplashScreen(QPixmap(Resources.getPath(Resources.Images, self.getApplicationName() + "view\images\hi.png")))

if __name__ == '__main__':
    app = QApplication(sys.argv) 
    ex = SlideShowPics()
    ex.show()
    sys.exit(app.exec_())