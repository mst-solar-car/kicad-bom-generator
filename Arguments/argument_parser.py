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
    if len(params) > 2:
      self.formatter = params[2].lower()
      # TODO: Verify formatter

    # Add verbose or debug
    if len(params) > 3:
      params[3] = params[3].lower()
      self.verbose = (params[3] == "verbose")
      self.debug = (params[3] == "debug")

    if len(params) > 4:
      params[4] = params[4].lower()
      self.verbose = (params[4] == "verbose" or self.verbose)
      self.debug = (params[4] == "debug" or self.debug)

    # Enforce trailing slash on project_folder
    lastChar = self.project_folder[len(self.project_folder) - 1:]
    if lastChar != "/" and lastChar != "\\":
      self.project_folder = self.project_folder + "/"
    elif lastChar == "\\":
      # Enforce a forward slash
      self.project_folder = self.project_folder[:-1] + "/"
