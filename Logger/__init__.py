__all__ = ['Log', 'Verbose', 'Debug', 'Fatal', 'Error', 'ToggleVerbose', 'ToggleDebug']

from .logger import *

logger = Logger()

def ToggleVerbose():
  """ Toggles verbose output on and off """
  logger.verbose = (not logger.verbose)
  Verbose("Verbose Output Enabled")

def ToggleDebug():
  """ Toggles debug output on and off """
  logger.debug = (not logger.debug)
  Debug("Debug Output Enabled")

def Log(*args):
  logger.Log(*args)

def Verbose(*args):
  logger.Verbose(*args)

def Debug(*args):
  logger.Debug(*args)

def Error(*args):
  logger.Error(*args)

def Fatal(*args):
  logger.Fatal(*args)