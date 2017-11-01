from Singleton import *
import Middleware


@Singleton
class FormatRegistrar:
  """ A class used to register, and apply formats """
  def __init__(self):
    self._formatters = {} # Start with nothing registered

  def Register(self, name, fn):
    """ Register a function that formats """
    print("Registering Formatter  " + name.lower())
    self._formatters[name.lower()] = fn

  def Dispatch(self, name):
    """ Wrapper function to wrap around doing formatting """
    name = name.lower()

    if name not in self._formatters:
      return None

    def dispatchWrapper(components):
      """ Wrapper function to call a formatter """
      return self._formatters[name](components)

    return dispatchWrapper


