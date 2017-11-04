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
    self._parser.add_argument("netlist", help='XML Netlist file that KiCad automatically generates. Use "%%I" in KiCad. This file is the input source for the parser')
    self._parser.add_argument("output", help='Name of the BOM File to generate (no extension). Use "%%O" in KiCad.')
    self._parser.add_argument("formatter", default=cfg['formatter'], help="Specify the formatter to use", nargs='?')
    self._parser.add_argument("-v", "--verbose", default=cfg.Get('verbose', False), help="Enable verbose output", action='count')
    self._parser.add_argument("-d", "--debug", default=cfg.Get('debug', False), help="Enable debugging output", action='count')
    self.args = self._parser.parse_args()

    if self.args.verbose >= 1:
      Logger.ToggleVerbose()

    if self.args.debug >= 1:
      Logger.ToggleDebug()

    self.output_file = self.args.output + "_BOM"

    self.formatter = self.args.formatter

    # Remove the generated XML file
    if not self.args.netlist.endswith(".xml"):
      Logger.Fatal("Must provide a netlist (.xml file) as input")

    self.input_file = self.args.netlist

    Logger.Verbose("Using netlist", self.input_file)

