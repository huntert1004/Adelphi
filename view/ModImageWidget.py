from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from util.DownloadThread import DownloadThread

class ModImageWidget(QWidget):
 """defines modimagewidget as a Qwidget"""
  def __init__(self, mod, parent=None):
      super().__init__()
      self.setMinimumSize(100, 67)
      self.pixmap = None
      self.mod = mod
      self.download_thread = DownloadThread(mod.imageUrl)
      self.download_thread.start()
      self.download_thread.data_downloaded.connect(self.ondownloadFinished)

  def paintEvent(self, paintEvent):
      """this added a paintevent to mod image"""
      painter = QPainter(self)
      if (self.pixmap):
          painter.drawPixmap(0, 0, self.pixmap)
         

  def ondownloadFinished(self):
       """defines ondownloadfinished"""
      self.paintImage()
     

  def paintImage(self):
     """paints Qpixmap"""
      pixmap = QPixmap()
      pixmap.loadFromData(self.download_thread.get_data())
      self.mod.image = pixmap
      self.setPixmap(pixmap)

  def setPixmap(self, pixmap):
     """sets Qpixmap"""
      self.pixmap = pixmap
      self.setMinimumSize(pixmap.width(), pixmap.height())
      self.update()
      
