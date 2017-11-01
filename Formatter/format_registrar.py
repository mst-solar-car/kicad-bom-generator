from Singleton import *
import Middleware


@Singleton
class FormatRegistrar:
  """ A class used to register, and apply formats """
  def __init__(self):
    self._formatters = {} # Start with nothing registered

  def normalize(self, s):
    return s.lower()

  def Register(self, name, fn):
    """ Register a function that formats """
    self._formatters[self.normalize(name)] = fn

  def Dispatch(self, name):
    """ Wrapper function to wrap around doing formatting """
    name = self.normalize(name)

    if name not in self._formatters:
      return None

    def dispatchWrapper(components):
      """ Wrapper function to call a formatter """
      return self._formatters[name](components)

    return dispatchWrapper


