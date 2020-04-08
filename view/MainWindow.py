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
from view.Browser import Browser
from view.Slides import Slides
from model.Mod import Mod


class MainWindow(QWidget):

  def searchMods(self):
    term = self.searchBar.text()
    print(term)
    if term:
      mods = ModsController.getSearchData(term)
      self.clearGrid()
      self.displayMods(mods)
    else:
      #FIXME this causes segmentation fault
      mods = ModsController.getModsData()
      self.clearGrid()
      self.displayMods(mods)
  def clearGrid(self):
    while self.grid.count():
      child = self.grid.takeAt(0)
      if child.widget():
        child.widget().deleteLater()

  def displayMods(self,mods):
    positions = [(i,j) for i in range(5) for j in range(4)]
            
    for position,item in zip(positions,mods):
            
      imageLabel = GridItem(self.parent)      
      imageLabel.mod.title = item['title']
      imageLabel.mod.description = item['body']
      imageLabel.mod.compat = item['field_minecraft_compatibility']
      imageLabel.mod.modfile = item['field_mod_file']
      imageLabel.mod.imageUrl = "https://minifymods.com" + item['field_screenshots']
      imageLabel.create(self)
      
      self.grid.addWidget(imageLabel, *position,)
      
  @pyqtSlot(QLabel)
  def topClicked(self, event):
    #print(event)
    modDetail = ModDetailsWindow(self.topmod)
    modDetail.setGeometry(100, 200, 100, 100)
    modDetail.setModal(True)
    #modDetail.show()
    mw = qtmodern.windows.ModernWindow(modDetail)
    mw.show()    
    
  def __init__(self, parent):
    super(MainWindow, self).__init__(parent)
    
     #get data for entire view
    mods = ModsController().getModsData()
    
    self.parent = parent
    self.layout = QVBoxLayout(self)

    #self.browser = Browser()
    #self.browser.setFixedSize(QSize(1200, 100))
    #self.browser.load("https://minifymods.com/ad.html")
    #self.layout.addWidget(self.browser)
    
    self.searchBar = QLineEdit()
    self.searchBar.setPlaceholderText("Search Mods") 
    self.searchBar.editingFinished.connect(self.searchMods)
    self.layout.addWidget(self.searchBar)
    
    # Initialize tab screen
    self.tabs = QTabWidget()
    self.tab1scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
    self.tab1widget = QWidget()                 # Widget that contains the collection of Vertical Box
    self.tab1vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons


    #add content into the tab1vbox
    #add top featured mod
    self.topmodLabel = QLabel("", self)
    self.topmodLabel.setGeometry(0, 0, 1200, 300)
    item = mods[0]
    imageUrl = "https://minifymods.com" + item['field_banner']
    image = QPixmap()
    image.loadFromData(urllib.request.urlopen(imageUrl).read())
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
    
    self.topmodLabel.mousePressEvent = self.topClicked
    
    #add row of other featured mods
    self.featuredModsWidget = QWidget()
    self.featuredModsLayout = QHBoxLayout()
    
    #2nd feature mod
    self.secondtopmod = QLabel("", self)
    self.secondtopmod.setGeometry(0, 0, 400, 300)
    secondimageUrl = "https://minifymods.com" + mods[1]['field_screenshots']
    secondimage = QPixmap()
    secondimage.loadFromData(urllib.request.urlopen(secondimageUrl).read())
    self.secondtopmod.setPixmap(secondimage.scaled(400, 300, Qt.KeepAspectRatio))
    self.featuredModsLayout.addWidget(self.secondtopmod)
    
    #3rd feature mod
    self.thirdtopmod = QLabel("", self)
    self.thirdtopmod.setGeometry(0, 0, 400, 300)
    thirdimageUrl = "https://minifymods.com" + mods[2]['field_screenshots']
    thirdimage = QPixmap()
    thirdimage.loadFromData(urllib.request.urlopen(thirdimageUrl).read())
    self.thirdtopmod.setPixmap(thirdimage.scaled(400, 300, Qt.KeepAspectRatio))
    self.featuredModsLayout.addWidget(self.thirdtopmod)
    
    #4th feature mod
    self.fourthtopmod = QLabel("", self)
    self.fourthtopmod.setGeometry(0, 0, 400, 300)
    fourthimageUrl = "https://minifymods.com" + mods[3]['field_screenshots']
    fourthimage = QPixmap()
    fourthimage.loadFromData(urllib.request.urlopen(fourthimageUrl).read())
    self.fourthtopmod.setPixmap(fourthimage.scaled(400, 300, Qt.KeepAspectRatio))
    self.featuredModsLayout.addWidget(self.fourthtopmod)
    
    self.featuredModsWidget.setLayout(self.featuredModsLayout)
    
    self.tab1vbox.addWidget(self.featuredModsWidget)

    #add grid
    self.gridWidget = QWidget()
    self.grid = QGridLayout()      
    
    self.displayMods(mods)
    
    self.gridWidget.setLayout(self.grid)
    self.tab1vbox.addWidget(self.gridWidget)
    
    
    ##### FINALIZE TAB1 #####
    #now set tab1widget layout
    self.tab1widget.setLayout(self.tab1vbox)
    
    # Add tabs
    self.tabs.addTab(self.tab1scroll,"Mods")
    #Scroll Area Properties
    self.tab1scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.tab1scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.tab1scroll.setWidgetResizable(True)
    self.tab1scroll.setWidget(self.tab1widget)
    
    
    #Finalize screen
    self.layout.addWidget(self.tabs)
    self.setLayout(self.layout)

    

  