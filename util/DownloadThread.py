import urllib.request
from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    """gets data"""
    data_downloaded = pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.url = url.split(", ")[0]
        self._data = None

    def run(self):
        """runs data"""
        self._data = urllib.request.urlopen(self.url).read()
        self.data_downloaded.emit()

    def get_data(self):
        return self._data