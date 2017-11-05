from Singleton import *
import Logger
from Component import *
from Utils import *

import tempfile
from shutil import copyfile
import os

@Singleton
class AfterwareRegistrar:
  """ A class used to register Afterware and dispatch Afterwaware """
  def __init__(self):
    self._afterware = {} # Start with nothing registered

  def Register(self, name, fn):
    """ Registers some afterware """
    name = normalizeStr(name)
    Logger.Debug("Registering Afterware:", name)
    self._afterware[name] = fn

  def Dispatch(self, name):
    """ Returns a function to wrap around afterware"""
    name = normalizeStr(name)

    if name not in self._afterware:
      return None

    def dispatchWrapper(savedFile):
      """ Wrapper Function to apply afterware """
      Logger.Debug("Running", name, "Afterware")

      try:
				self._afterware[name](savedFile)
				return savedFile

      except Exception as e:
        Logger.Error("Exception", e, "in", name, "Afterware")
        return savedFile

    return dispatchWrapper
