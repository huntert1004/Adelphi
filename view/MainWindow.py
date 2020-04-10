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
   
  @pyqtSlot(QLabel)
  def secondClicked(self, event):
  #print(event)
    modDetail = ModDetailsWindow(self.secondtopmod)
    modDetail.setGeometry(100, 200, 100, 100)
    modDetail.setModal(True)
    #modDetail.show()
    mw = qtmodern.windows.ModernWindow(modDetail)
    mw.show() 
  @pyqtSlot(QLabel)
  def thirdClicked(self, event):
  #print(event)
    modDetail = ModDetailsWindow(self.thirdtopmod)
    modDetail.setGeometry(100, 200, 100, 100)
    modDetail.setModal(True)
    #modDetail.show()
    mw = qtmodern.windows.ModernWindow(modDetail)
    mw.show()
  @pyqtSlot(QLabel)
  def fourthClicked(self, event):
  #print(event)
    modDetail = ModDetailsWindow(self.fourthtopmod)
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
    item = mods[1]
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
    item = mods[3]
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

    

  