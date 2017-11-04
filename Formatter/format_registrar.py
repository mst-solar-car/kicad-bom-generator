from Singleton import *
import Logger
from Utils import *

@Singleton
class FormatRegistrar:
  """ A class used to register, and apply formats """
  def __init__(self):
    self._formatters = {} # Start with nothing registered

  def Register(self, name, fn):
    """ Register a function that formats """
    name = normalizeStr(name)
    Logger.Debug("Registering Formatter:", name)
    self._formatters[name] = fn

  def Dispatch(self, name):
    """ Wrapper function to wrap around doing formatting """
    name = normalizeStr(name)

    if name not in self._formatters:
      return None

    def dispatchWrapper(components):
      """ Wrapper function to call a formatter """
      Logger.Debug("Running", name, "Formatter")

      try:
        return self._formatters[name](components)
      except Exception as e:
        Logger.Error("Exception", e, "in", name, "Formatter")

    return dispatchWrapper


