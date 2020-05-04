import json
import urllib.request
import os
import platform
from pathlib import Path

class ModsController:
  __instance = None
  @staticmethod 
  def getInstance():
    """ Static access method. """
    if ModsController.__instance == None:
        ModsController()
    return ModsController.__instance


  @staticmethod
  def getCompatFilter(filter=""):
    compatFilter = "" if filter=="" else "&compat="+filter
    if (filter == "Filter by Minecraft Version"):
      compatFilter = ""
    return compatFilter

  @staticmethod
  def getModsData(page=0,filter=""):
    json_url = "https://minifymods.com/api/mods?_format=json&page=" + str(page) + ModsController.getCompatFilter(filter)
    data = urllib.request.urlopen(json_url).read().decode()
    return json.loads(data)

  @staticmethod
  def getSearchData(term,filter=""):
    json_url = "https://minifymods.com/api/mods?_format=json&search=" + term + ModsController.getCompatFilter(filter)
    data = urllib.request.urlopen(json_url).read().decode()
    return json.loads(data)
    
  def __init__(self):
    """ Virtually private constructor. """
    if ModsController.__instance != None:
        raise Exception("This class is a singleton!")
    else:
        ModsController.__instance = self


  @staticmethod
  def getVersionsDirectory():
        if platform.system() == 'Windows':
            appData = os.getenv('APPDATA')
            directory = appData + "\\.minecraft\\versions"
        elif platform.system() == "Darwin":
            appData = str(Path.home())
            directory = appData + "/Library/Application Support/minecraft/versions"
        elif platform.system() == "Linux":
            appData = str(Path.home())
            directory = appData + "/.minecraft/versions"
        return directory

  @staticmethod
  def getDotMinecraftDirectory():
    if platform.system() == 'Windows':
        appData = os.getenv('APPDATA')
        directory = appData + "\\.minecraft\\"
    elif platform.system() == "Darwin":
        appData = str(Path.home())
        directory = appData + "/Library/Application Support/minecraft/"
    elif platform.system() == "Linux":
        appData = str(Path.home())
        directory = appData + "/.minecraft/"
    return directory

  @staticmethod
  def getModDirectory():
    if platform.system() == 'Windows':
      appData = os.getenv('APPDATA')
      directory = appData + "\\.minecraft\\mods\\"
    elif platform.system() == "Darwin":
      appData = str(Path.home())
      directory = appData + "/Library/Application Support/minecraft/mods"
    elif platform.system() == "Linux":
      appData = str(Path.home())
      directory = appData + "/.minecraft/mods"
    return directory
  


    