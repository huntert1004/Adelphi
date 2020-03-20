import json
import urllib.request

class ModsController:
  __instance = None
  @staticmethod 
  def getInstance():
    """ Static access method. """
    if ModsController.__instance == None:
        ModsController()
    return ModsController.__instance

  @staticmethod
  def getModsData():
    json_url = "https://minifymods.com/api/mods?_format=json"
    data = urllib.request.urlopen(json_url).read().decode()
    return json.loads(data)

  def __init__(self):
    """ Virtually private constructor. """
    if ModsController.__instance != None:
        raise Exception("This class is a singleton!")
    else:
        ModsController.__instance = self