import sys
import os

import Config
from Singleton import *

args = sys.argv[1:]

cfg = Config.Get()

@Singleton
class ArgumentParser:
  """ A class to get and represent arguments sent to the program """
  def __init__(self):
    """ Constructor """
    self.project_folder = os.path.split(os.path.abspath(args[1]))[0]
    self.formatter = cfg["defaultFormatter"]
    self.verbose = False
    self.debug = False

    os.remove(args[0]) # Remove the generated XML file

    # Add formatter if there is one
    if len(args) > 2:
      self.formatter = args[2].lower()
      # TODO: Verify formatter

    # Add verbose or debug
    if len(args) > 3:
      if args[3].lower() == "verbose":
        self.verbose = True
      elif args[3].lower() == "debug":
        self.debug = True

    if len(args) > 4:
      if args[4].lower() == "verbose":
        self.verbose = True
      elif args[4].lower() == "debug":
        self.debug = True

    # Enforce trailing slash on project_folder
    lastChar = self.project_folder[len(self.project_folder) - 1:]
    if lastChar != "/" and lastChar != "\\":
      self.project_folder = self.project_folder + "/"

