import os
import json
from Singleton import Singleton
from Utils import *

folder = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0] # Parent folder (home of config.json)
config_file = "{0}/config.json".format(folder)

@Singleton
class Configuration:
  """ Represents program configuration """
  def __init__(self):
    try:
      # Attempt to load from the ocnfig file
      with open(config_file, 'r') as config:
        self.raw_data = config.read().replace('\n', '').replace('\r', '')
      self.data = json.loads(self.raw_data)
    except:
      self.data = {}

    # Create entries for these if they don't exist
    self.Get('formatter', '')
    self.Get('middleware', [])
    self.Get('columns', [])
    self.Get('metadataAliases', {})
    self.Get('emptyValue', '')
    self.Get('outputLineSeparator', '\\n')

    # Normalize strings
    self.data['formatter'] = normalizeStr(self.data['formatter'])
    self.data['middleware'] = [ normalizeStr(m) for m in self.data['middleware'] ]
    self.data['metadataAliases'] = { normalizeStr(key): normalizeStr(value) for key, value in self.data['metadataAliases'].items() }
    self.data['columns'] = [ normalizeStr(c) for c in self.data['columns'] ]

  def Get(self, key, defaultValue=None):
    """ Retrieve an item or set a value if it doesn't exist """
    if key not in self.data:
      self.data[key] = defaultValue

    return self.data[key]

  def __getitem__(self, key):
    """ Index operator """
    if key not in self.data:
      return None

    return self.data[key]

  def __setitem__(self, key, value):
    """ Index Operator """
    self.data[key] = value