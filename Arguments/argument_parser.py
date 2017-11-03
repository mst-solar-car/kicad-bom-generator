import sys
import os
from copy import deepcopy

import argparse

import Config
import Logger
from Singleton import *


cfg = Config.Get()


@Singleton
class ArgumentParser:
  """ A class to get and represent arguments sent to the program """
  def __init__(self, *args, **kwargs):
    self._parser = argparse.ArgumentParser(description="KiCad Bill-Of-Materials Generator")
    self._parser.add_argument("netlist", help='XML Netlist file that KiCad automatically generates. Use "%%I" in KiCad. If specified the file will be removed. Leave as a space to ignore')
    self._parser.add_argument("output", help='Name of the BOM File to generate (no extension). Use "%%O" in KiCad. This should be in the same folder as the .pro file')
    self._parser.add_argument("formatter", default=cfg['formatter'], help="Specify the formatter to use")
    self._parser.add_argument("-v", "--verbose", default=cfg.Get('verbose', False), help="Enable verbose output", action='count')
    self._parser.add_argument("-d", "--debug", default=cfg.Get('debug', False), help="Enable debugging output", action='count')
    self.args = self._parser.parse_args()

    if self.args.verbose >= 1:
      Logger.ToggleVerbose()

    if self.args.debug >= 1:
      Logger.ToggleDebug()

    self.output_file = self.args.output + "_BOM"

    # Get the name of the project file (.pro file)
    self.project_file = self.args.output
    if not self.project_file.endswith(".pro"):
      self.project_file = self.project_file + ".pro"

    # Verify .pro file exists
    if not os.path.isfile(self.project_file):
      Logger.Fatal("Paramter for output, '{0}', needs to be the name of the .pro file".format(self.args.output))

    self.formatter = self.args.formatter

    # Remove the generated XML file
    if self.args.netlist.endswith(".xml"):
      try:
        os.remove(self.args.netlist)
      except:
        Logger.Error("Could not remove {0}".format(self.args.netlist))

    # Get parent folder of the .pro file
    self.project_folder = os.path.split(os.path.abspath(self.project_file))[0]

    # Enforce trailing slash on project_folder
    lastChar = self.project_folder[len(self.project_folder) - 1:]
    if lastChar != "/" and lastChar != "\\":
      self.project_folder = self.project_folder + "/"
    elif lastChar == "\\":
      # Enforce a forward slash
      self.project_folder = self.project_folder[:-1] + "/"

    Logger.Verbose("Project Folder:", self.project_folder)

