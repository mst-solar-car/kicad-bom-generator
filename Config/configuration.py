import os
import json
from Singleton import Singleton

folder = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0] # Parent folder (home of config.json)
config_file = "{0}/config.json".format(folder)

@Singleton
class Configuration:
  """ Represents program configuration """
  def __init__(self):
    with open(config_file, 'r') as config:
        self.raw_data = config.read().replace('\n', '').replace('\r', '')

    self.data = json.loads(self.raw_data)