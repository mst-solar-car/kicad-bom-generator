import sys
import os
from copy import deepcopy
import argparse

import Config
import Logger
from Singleton import *
from Utils import *


cfg = Config.Get()


@Singleton
class ArgumentParser:
  """ A class to get and represent arguments sent to the program """
  def __init__(self, *args, **kwargs):
    self._parser = argparse.ArgumentParser(description="KiCad Bill-Of-Materials Generator")
    self._parser.add_argument("netlist", help='XML Netlist file that KiCad automatically generates. Use "%%I" in KiCad. This file is the input source for the parser')
    self._parser.add_argument("output", help='Name of the BOM File to generate (with formatter extension). Use "%%O.extension" in KiCad.')
    self._parser.add_argument("formatter", default=cfg['formatter'], help="Specify the formatter to use", nargs='?')
    self._parser.add_argument("-v", "--verbose", default=cfg.Get('verbose', False), help="Enable verbose output", action='count')
    self._parser.add_argument("-d", "--debug", default=cfg.Get('debug', False), help="Enable debugging output", action='count')
    self.args = self._parser.parse_args()

    if self.args.verbose >= 1:
      Logger.ToggleVerbose()

    if self.args.debug >= 1:
      Logger.ToggleDebug()

    self.output_file = self.args.output

    # Get the formatter (extension)
    extension = os.path.splitext(self.output_file)[1]
    self.formatter = normalizeStr(extension).strip('.')

    # If no formatter is specified then use the one in the config file
    if self.formatter == "":
      self.formatter = cfg.Get('formatter', 'No Formatter')
      self.output_file = self.output_file + "." + self.formatter

    Logger.Verbose("Using", self.formatter, "formatter")

    # Remove the generated XML file
    if not self.args.netlist.endswith(".xml"):
      Logger.Fatal("Must provide a netlist (.xml file) as input")

    self.input_file = self.args.netlist

    Logger.Verbose("Using netlist", self.input_file)

