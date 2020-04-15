from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.DownloadThread import DownloadThread

class ModImageWidget(QWidget):
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
