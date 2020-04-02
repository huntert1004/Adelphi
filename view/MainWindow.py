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

from view.GridItem import GridItem
from view.ListItem import ListItem
from controller.ModsController import ModsController
from view.Browser import Browser
from view.Slides import Slides

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
      imageUrl = "https://minifymods.com" + item['field_screenshots']
      image = QPixmap()
      image.loadFromData(urllib.request.urlopen(imageUrl).read())
      imageLabel = GridItem(self.parent)
      
      imageLabel.title = item['title']
      imageLabel.description = item['body']
      imageLabel.compat = item['field_minecraft_compatibility']
      imageLabel.modfile = item['field_mod_file']
      imageLabel.image = image           
      imageLabel.setPixmap(image.scaled(300, 200, Qt.KeepAspectRatio))
      imageLabel.setFixedSize(300, 200)
      imageLabel.mousePressEvent = imageLabel.Clicked
      
      self.grid.addWidget(imageLabel, *position)

  def __init__(self, parent):
    super(MainWindow, self).__init__(parent)
    self.parent = parent
    self.layout = QVBoxLayout(self)

    self.browser = Browser()
    self.browser.setFixedSize(QSize(1200, 100))
    self.browser.load("https://minifymods.com/ad.html")
    self.layout.addWidget(self.browser)
    
    self.searchBar = QLineEdit()
    self.searchBar.setPlaceholderText("Search Mods") 
    self.searchBar.editingFinished.connect(self.searchMods)
    self.layout.addWidget(self.searchBar)
    # Initialize tab screen
    self.tabs = QTabWidget()
    self.tab1 = QScrollArea()
    self.tab2 = QWidget()
    self.tabs.resize(300,200)
    self.tab1.setWidgetResizable(True)
    
    # Add tabs
    self.tabs.addTab(self.tab1,"Mods")
    #self.tabs.addTab(self.tab2,"Tab 2")
    
    # Create first tab
    self.tab1.layout = QVBoxLayout(self)
    self.grid = QGridLayout()
    #self.listWidget = ListItem()

    slidemods = mods[:5]
    image_files = []
    for mod in slidemods:
      imageUrl = "https://minifymods.com" + mod['field_screenshots']
      image_files.append(imageUrl)

    self.slides_widget = Slides(image_files, self)
    self.layout.addWidget(slides_widget)
    #listmods = mods[9:len(mods)]


    #get data
    mods = ModsController().getModsData()
    self.displayMods(mods)
  
      #TODO loop over listmods and add to an instance of myListWidget

      #possibly do this
      #self.grid.addWidget(listWidget)

    self.tab1.layout.addLayout(self.grid)
    self.tab1.setLayout(self.tab1.layout)
    # add grid to tab1
    # Add tabs to widget
    self.layout.addWidget(self.tabs)
    self.setLayout(self.layout)
      
  