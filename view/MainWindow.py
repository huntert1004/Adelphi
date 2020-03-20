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

class MainWindow(QWidget):
          
  def __init__(self, parent):
    super(MainWindow, self).__init__(parent)
    self.layout = QVBoxLayout(self)

    # Initialize tab screen
    self.tabs = QTabWidget()
    self.tab1 = QScrollArea()
    self.tab2 = QWidget()
    self.tabs.resize(300,200)
    self.tab1.setWidgetResizable(True)
    
    # Add tabs
    self.tabs.addTab(self.tab1,"Tab 1")
    self.tabs.addTab(self.tab2,"Tab 2")
    
    # Create first tab
    self.tab1.layout = QVBoxLayout(self)
    self.grid = QGridLayout()
    self.listWidget = ListItem()
    #get data
    json_url = "https://minifymods.com/api/mods?_format=json"
    data = urllib.request.urlopen(json_url).read().decode()
    mods = json.loads(data);
    #gridmods = mods[:9]
    #listmods = mods[9:len(mods)]


    positions = [(i,j) for i in range(5) for j in range(4)]
            
    for position,item in zip(positions,mods):
      imageUrl = "https://minifymods.com" + item['field_screenshots']
      image = QPixmap()
      image.loadFromData(urllib.request.urlopen(imageUrl).read())
      imageLabel = GridItem(parent)
      
      imageLabel.title = item['title']
      imageLabel.description = item['body']
      imageLabel.compat = item['field_minecraft_compatibility']
      imageLabel.modfile = item['field_mod_file']
      imageLabel.image = image           
      imageLabel.setPixmap(image.scaled(300, 200, Qt.KeepAspectRatio))
      imageLabel.setFixedSize(300, 200)
      imageLabel.mousePressEvent = imageLabel.Clicked
      
      self.grid.addWidget(imageLabel, *position)
  
      #TODO loop over listmods and add to an instance of myListWidget

      #possibly do this
      #self.grid.addWidget(listWidget)

    self.tab1.layout.addLayout(self.grid)
    self.tab1.setLayout(self.tab1.layout)
    # add grid to tab1
    # Add tabs to widget
    self.layout.addWidget(self.tabs)
    self.setLayout(self.layout)
      
  