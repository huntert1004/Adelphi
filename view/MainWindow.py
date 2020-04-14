import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os
import shutil
import urllib.request
import qtmodern.styles
import qtmodern.windows
from pathlib import Path
from view.ModDetailsWindow import ModDetailsWindow
from view.GridItem import GridItem
from view.ListItem import ListItem
from controller.ModsController import ModsController
#from view.Browser import Browser
from view.Slides import Slides
from model.Mod import Mod

class MainWindow(QWidget):

  def searchMods(self):
    term = self.searchBar.text()
    
    if term:
      mods = ModsController.getSearchData(term, self.filterSelect.currentText())
      self.createSearchTab()
      self.displaySearch(mods)

  def createSearchTab(self):
    if not hasattr(self, 'searchTabScroll'):
      self.searchTabScroll = QScrollArea()
      self.searchTabWidget = QWidget()
      self.searchTabVBoxLayout = QVBoxLayout()

      # Add tabs
      self.searchTabWidget.setLayout(self.searchTabVBoxLayout)
      self.tabs.addTab(self.searchTabScroll,"Search")
      self.tabs.setCurrentIndex(self.tabs.count()-1)
      self.tabs.tabBar().setTabButton(self.tabs.count()-1, QTabBar.RightSide,None)
      #Scroll Area Properties
      self.searchTabVBoxLayout.setAlignment(Qt.AlignTop)
      self.searchTabScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
      self.searchTabScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
      self.searchTabScroll.setWidgetResizable(True)
      self.searchTabScroll.setWidget(self.searchTabWidget)
    
    self.clearSearchResults()    
  
  def clearGrid(self):
    self.page = 0
    self.loadMoreButton.setEnabled(True)
    self.loadMoreButton.setText("Load More")
    while self.grid.count():
      child = self.grid.takeAt(0)
      if child.widget():
        child.widget().deleteLater()
  
  def clearSearchResults(self):
    while self.searchTabVBoxLayout.count():
      child = self.searchTabVBoxLayout.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

    self.searchTitle = QLabel("Search Results")
    self.searchTitle.setStyleSheet("font-weight: bold; font-size: 200%")
    self.searchTabVBoxLayout.addWidget(self.searchTitle)

  def displaySearch(self,mods):
    #positions = [(i,j) for i in range(5) for j in range(4)]
            
    #for position,item in zip(positions,mods):
    for item in mods:
      resultWidget = QWidget()
      resultLayout = QHBoxLayout()
      resultLayout.setAlignment(Qt.AlignLeft)
      
      mod = Mod() 
      mod.title = item['title']
      mod.description = item['body']
      mod.compat = item['field_minecraft_compatibility']
      mod.modfile = item['field_mod_file']
      mod.imageUrl = "https://minifymods.com" + item['field_screenshots']
      mod.image = QPixmap()
      mod.image.loadFromData(urllib.request.urlopen(mod.imageUrl).read())
      
      @pyqtSlot(QLabel)
      def searchClick(event):
        self.modClicked(mod)
      
      imageLabel = QLabel()
      imageLabel.setPixmap(mod.image.scaled(100, 67, Qt.KeepAspectRatio))
      imageLabel.mousePressEvent = searchClick
      resultLayout.addWidget(imageLabel)

      textLabel = QLabel(item['title'])
      resultLayout.addWidget(textLabel)
      
      resultWidget.setLayout(resultLayout)
      self.searchTabVBoxLayout.addWidget(resultWidget)
  
  @pyqtSlot()
  def loadMore(self):
    if self.page > 5:
      return
    self.page += 1
    mods = ModsController.getModsData(self.page,self.filterSelect.currentText())
    self.displayMods(mods)

  def displayMods(self,mods):
    if self.page > 5:
      return
    rowRange = range(5)
    if self.page == 1:
      rowRange = range(6,10)
    if self.page == 2:
      rowRange = range(11,15)
    if self.page == 3:
      rowRange = range(16,20)
    if self.page == 4:
      rowRange = range(21,25)
    if self.page == 5:
      rowRange = range(26,30)
      self.loadMoreButton.setEnabled(False)
      self.loadMoreButton.setText("Try Searching!")
    
    positions = [(i,j) for i in rowRange for j in range(4)]
            
    for position,item in zip(positions,mods):
      imageLabel = GridItem(self)      
      imageLabel.mod.title = item['title']
      imageLabel.mod.description = item['body']
      imageLabel.mod.compat = item['field_minecraft_compatibility']
      imageLabel.mod.modfile = item['field_mod_file']
      imageLabel.mod.imageUrl = "https://minifymods.com" + item['field_screenshots']
      imageLabel.create(self)
      
      self.grid.addWidget(imageLabel, *position)
  
  def closeTab (self, currentIndex):
    currentQWidget = self.tabs.widget(currentIndex)
    currentQWidget.deleteLater()
    self.tabs.removeTab(currentIndex)


  @pyqtSlot(QLabel)
  def modClicked(self, mod):
    modDetail = ModDetailsWindow(mod)
    self.tabs.addTab(modDetail,mod.title)    
    self.tabs.setCurrentIndex(self.tabs.count()-1)


  @pyqtSlot(QLabel)
  def topClicked(self, event):
    self.modClicked(self.topmod)
     
  @pyqtSlot(QLabel)
  def secondClicked(self, event):
    self.modClicked(self.secondtopmod)
  
  @pyqtSlot(QLabel)
  def thirdClicked(self, event):
    self.modClicked(self.thirdtopmod)
  
  @pyqtSlot(QLabel)
  def fourthClicked(self, event):
    self.modClicked(self.fourthtopmod)

  @pyqtSlot()
  def filterChanged(self, *args):    
    mods = ModsController.getModsData(0,self.filterSelect.currentText())
    self.clearGrid()
    self.displayMods(mods)
    
  def __init__(self, parent,*args, **kwargs):
    super().__init__()

    self.title = 'Adellphi'
    self.left = 0
    self.top = 0
    self.width = 1280
    self.height = 900
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)

    self.page = 0
    
     #get data for entire view
    mods = ModsController().getModsData()
    
    self.parent = parent
    self.layout = QVBoxLayout(self)

    #self.browser = Browser()
    #self.browser.setFixedSize(QSize(1200, 100))
      
    #self.browser.load("https://minifymods.com/ad.html")
    #self.layout.addWidget(self.browser)
    self.topBarWidget = QWidget(self)
    self.topBarLayout = QHBoxLayout(self)

    self.searchBar = QLineEdit()
    self.searchBar.setPlaceholderText("Search Mods") 
    self.searchBar.editingFinished.connect(self.searchMods)
    self.topBarLayout.addWidget(self.searchBar)

    self.filterSelect = QComboBox()
    self.filterSelect.addItem("Filter by Minecraft Version")
    self.filterSelect.addItems(["1.12.2","1.15.2","1.7.10","1.8.9"])
    self.filterSelect.currentIndexChanged.connect(self.filterChanged)
    self.topBarLayout.addWidget(self.filterSelect)

    self.topBarWidget.setLayout(self.topBarLayout)
    self.layout.addWidget(self.topBarWidget)
    
    # Initialize tab screen
    self.tabs = QTabWidget()
    self.tabs.setTabsClosable(True)
    self.tabs.tabCloseRequested.connect(self.closeTab)
    

    self.tab1scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
    self.tab1widget = QWidget()                 # Widget that contains the collection of Vertical Box
    self.tab1vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons


    #add content into the tab1vbox
    #add top featured mod
    
    self.topmodLabel = QLabel("", self)
    self.topmodLabel.setGeometry(0, 0, 1200, 300)
    item = mods[0]
    image = QPixmap("images/New Project.png")
    self.topmodLabel.setPixmap(image.scaled(1200, 400, Qt.KeepAspectRatio))
    self.tab1vbox.addWidget(self.topmodLabel)
    self.topmod = Mod()
    self.topmod.title = item['title']
    self.topmod.description = item['body']
    self.topmod.compat = item['field_minecraft_compatibility']
    self.topmod.modfile = item['field_mod_file']
    self.topmod.imageUrl = "https://minifymods.com" + item['field_screenshots']
    self.topmod.image = QPixmap()
    self.topmod.image.loadFromData(urllib.request.urlopen(self.topmod.imageUrl).read())
    
    
    
    #add row of other featured mods
    self.featuredModsWidget = QWidget()
    self.featuredModsLayout = QHBoxLayout()
    
    #2nd feature mod
    self.secondtopmodlabel = QLabel("", self)
    self.secondtopmodlabel.setGeometry(0, 0, 400, 300)
    item = mods[0]
    secondimageUrl = "https://minifymods.com" + item['field_screenshots']
    image = QPixmap()
    image.loadFromData(urllib.request.urlopen(secondimageUrl).read())
    self.secondtopmodlabel.setPixmap(image.scaled(400, 300, Qt.KeepAspectRatio))
    self.featuredModsLayout.addWidget(self.secondtopmodlabel)
    self.secondtopmod = Mod()
    self.secondtopmod.title = item['title']
    self.secondtopmod.description = item['body']
    self.secondtopmod.compat = item['field_minecraft_compatibility']
    self.secondtopmod.modfile = item['field_mod_file']
    self.secondtopmod.imageUrl = "https://minifymods.com" + item['field_screenshots']
    self.secondtopmod.image = QPixmap()
    self.secondtopmod.image.loadFromData(urllib.request.urlopen(self.secondtopmod.imageUrl).read())
    
    self.secondtopmodlabel.mousePressEvent = self.secondClicked
    #3rd feature mod
    self.thirdtopmodlabel = QLabel("", self)
    self.thirdtopmodlabel.setGeometry(0, 0, 400, 300)
    item = mods[2]
    thirdimageUrl = "https://minifymods.com" + item['field_screenshots']
    thirdimage = QPixmap()
    thirdimage.loadFromData(urllib.request.urlopen(thirdimageUrl).read())
    self.thirdtopmodlabel.setPixmap(thirdimage.scaled(400, 300, Qt.KeepAspectRatio))
    self.featuredModsLayout.addWidget(self.thirdtopmodlabel)
    self.thirdtopmod = Mod()
    self.thirdtopmod.title = item['title']
    self.thirdtopmod.description = item['body']
    self.thirdtopmod.compat = item['field_minecraft_compatibility']
    self.thirdtopmod.modfile = item['field_mod_file']
    self.thirdtopmod.imageUrl = "https://minifymods.com" + item['field_screenshots']
    self.thirdtopmod.image = QPixmap()
    self.thirdtopmod.image.loadFromData(urllib.request.urlopen(self.thirdtopmod.imageUrl).read())
    
    self.thirdtopmodlabel.mousePressEvent = self.thirdClicked
    
    #4th feature mod
    self.fourthtopmodlabel = QLabel("", self)
    self.fourthtopmodlabel.setGeometry(0, 0, 400, 300)
    item = mods[4]
    fourthimageUrl = "https://minifymods.com" + item['field_screenshots']
    fourthimage = QPixmap()
    fourthimage.loadFromData(urllib.request.urlopen(fourthimageUrl).read())
    self.fourthtopmodlabel.setPixmap(fourthimage.scaled(400, 300, Qt.KeepAspectRatio))
    self.featuredModsLayout.addWidget(self.fourthtopmodlabel)
    self.fourthtopmod = Mod()
    self.fourthtopmod.title = item['title']
    self.fourthtopmod.description = item['body']
    self.fourthtopmod.compat = item['field_minecraft_compatibility']
    self.fourthtopmod.modfile = item['field_mod_file']
    self.fourthtopmod.imageUrl = "https://minifymods.com" + item['field_screenshots']
    self.fourthtopmod.image = QPixmap()
    self.fourthtopmod.image.loadFromData(urllib.request.urlopen(self.fourthtopmod.imageUrl).read())
    
    self.fourthtopmodlabel.mousePressEvent = self.fourthClicked
    
    
    
    self.featuredModsWidget.setLayout(self.featuredModsLayout)
    
    self.tab1vbox.addWidget(self.featuredModsWidget)

    #add grid
    self.gridWidget = QWidget()
    self.grid = QGridLayout()      
    
    self.displayMods(mods)
    
    self.gridWidget.setLayout(self.grid)
    self.tab1vbox.addWidget(self.gridWidget)
    
    #add load more button
    self.loadMoreButton = QPushButton("Load More")
    self.loadMoreButton.clicked.connect(self.loadMore)
    self.tab1vbox.addWidget(self.loadMoreButton)
    
    ##### FINALIZE TAB1 #####
    #now set tab1widget layout
    self.tab1widget.setLayout(self.tab1vbox)
    self.tab1scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.tab1scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tab1scroll.setWidgetResizable(True)
    self.tab1scroll.setWidget(self.tab1widget)
    # Add tabs
    self.tabs.addTab(self.tab1scroll,"Mods")
    #make the first tab not closeable
    self.tabs.tabBar().setTabButton(0, QTabBar.RightSide,None)

    #Scroll Area Properties
    def scrollevent(self,event):
      if event.key() == QtCore.Qt.Key_Down:
              if self.tab1scroll.currentRow() == self.count()-1:
                  self.tab1scroll.setCurrentRow(0)
                  return
              elif event.key() == QtCore.Qt.Key_Up:
                  if self.tab1scroll.currentRow() == 0:
                      self.tab1scroll.setCurrentRow(self.count()-1)
                      return

        # Otherwise, parent behavior
                      super().scrollevent(event)
    
    
    #Finalize screen
    self.layout.addWidget(self.tabs)
    self.setLayout(self.layout)
      
    

  