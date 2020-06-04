import PyQt5
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5.QtWebEngineWidgets import QWebEngineSettings as QWebSettings
from PyQt5.QtNetwork import *

class Browser(QWebView):
    """addes ad too qmainwindow""""
    def __init__(self):
        # QWebView
        self.view = QWebView.__init__(self)
        #self.view.setPage(MyBrowser())
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)
        #super(Browser).connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&amp;)"), self.adjustTitle)

    def load(self,url):
        self.setUrl(QUrl(url))
    
    def adjustTitle(self):
        self.setWindowTitle(self.title())
    
    def disableJS(self):
        """disables JS"""
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.JavascriptEnabled, False)
        