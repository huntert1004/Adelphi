from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from view.ModDetailsWindow import ModDetailsWindow
from model.Mod import Mod
import qtmodern

from util.DownloadThread import DownloadThread

class GridItem(QWidget):
    mod = None     
    
    def __init__(self, parent):
      super().__init__()
      self.parent = parent
      self.mod = Mod()
      self.setFixedSize(300, 250)
    
    def create(self, parent):      
      self.layout = QVBoxLayout()
      self.imageLabel = ImageLabel(self.mod)
      self.imageLabel.mousePressEvent = self.clicked      
      self.layout.addWidget(self.imageLabel)
      self.textLabel = QLabel(self.mod.title)
      self.textLabel.mousePressEvent = self.clicked
      self.textLabel.setFixedSize(300, 20)
      self.layout.addWidget(self.textLabel)
      self.setLayout(self.layout)

    @pyqtSlot(QLabel)
    def clicked(self,event):
      modDetail = ModDetailsWindow(self.mod)
      self.parent.tabs.addTab(modDetail,self.mod.title)    
      self.parent.tabs.setCurrentIndex(self.parent.tabs.count()-1)

class ImageLabel(QWidget):
  def __init__(self, mod, parent=None):
      super().__init__()
      self.setMinimumSize(50, 50)
      self.pixmap = None
      self.mod = mod
      self.download_thread = DownloadThread(mod.imageUrl)
      self.download_thread.start()
      self.download_thread.data_downloaded.connect(self.ondownloadFinished)

  def paintEvent(self, paintEvent):
      painter = QPainter(self)
      if (self.pixmap):
          painter.drawPixmap(0, 0, self.pixmap)

  def ondownloadFinished(self):
      self.paintImage()

  def paintImage(self):
      pixmap = QPixmap()
      pixmap.loadFromData(self.download_thread.get_data())
      self.mod.image = pixmap
      self.setPixmap(pixmap)

  def setPixmap(self, pixmap):
      self.pixmap = pixmap
      self.setMinimumSize(pixmap.width(), pixmap.height())
      self.update()
