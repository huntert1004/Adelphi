import json
import urllib.request
import os
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
        if os.name == 'nt':
            appData = os.getenv('APPDATA')
            versions_directory = appData + "\\.minecraft\\versions"
        else:
            appData = str(Path.home())
            versions_directory = appData + "/.minecraft/versions"
        return versions_directory

  @staticmethod
  def getDotMinecraftDirectory():
        if os.name == 'nt':
            appData = os.getenv('APPDATA')
            versions_directory = appData + "\\.minecraft\\"
        else:
            appData = str(Path.home())
            versions_directory = appData + "/.minecraft/"
        return versions_directory

  @staticmethod
  def getModDirectory():
    if os.name == 'nt':
        appData = os.getenv('APPDATA')
        mod_directory = appData + "\\.minecraft\\mods\\"
    else:
        appData = str(Path.home())
        mod_directory = appData + "/.minecraft/mods/"
    return mod_directory
  


    