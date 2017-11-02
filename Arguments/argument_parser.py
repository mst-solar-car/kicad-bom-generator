import sys
import os

import Config
from Singleton import *

from copy import deepcopy

cfg = Config.Get()

@Singleton
class ArgumentParser:
  """ A class to get and represent arguments sent to the program """
  def __init__(self, *args, **kwargs):
    """ Constructor """
    params = args[0]
    for p in params:
      print("HI", p)

    if len(params) < 2:
      params.append("") # Path to XML file that doesn't exist
      params.append(os.getcwd())

    self.project_folder = os.path.split(os.path.abspath(params[1]))[0]
    self.formatter = cfg["defaultFormatter"]
    self.verbose = False
    self.debug = False

    try:
      os.remove(params[0]) # Remove the generated XML file
    except:
      pass

    # Add formatter if there is one
    if len(args) > 2:
      self.formatter = params[2].lower()
      # TODO: Verify formatter

    # Add verbose or debug
    if len(params) > 3:
      if params[3].lower() == "verbose":
        self.verbose = True
      elif params[3].lower() == "debug":
        self.debug = True

    if len(params) > 4:
      if params[4].lower() == "verbose":
        self.verbose = True
      elif params[4].lower() == "debug":
        self.debug = True

    # Enforce trailing slash on project_folder
    lastChar = self.project_folder[len(self.project_folder) - 1:]
    if lastChar != "/" and lastChar != "\\":
      self.project_folder = self.project_folder + "/"
    elif lastChar == "\\":
      # Enforce a forward slash
      self.project_folder = self.project_folder[:-1] + "/"
