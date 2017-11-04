from Singleton import *
import Logger
from Component import *
from Utils import *

@Singleton
class MiddlewareRegistrar:
  """ A class used to register Middleware and dispatch Middleware """
  def __init__(self):
    self._middleware = {} # Start with nothing registered

  def Register(self, name, fn):
    """ Registers some middleware """
    name = normalizeStr(name)
    Logger.Debug("Registering Middleware:", name)
    self._middleware[name] = fn

  def Dispatch(self, name):
    """ Returns a function to wrap around middleware """
    name = normalizeStr(name)

    if name not in self._middleware:
      return None

    def dispatchWrapper(components):
      """ Wrapper Function to apply middleware """
      cpy = components.Copy() # Create a copy of the component list (to continue in pipeline if failure)
      Logger.Debug("Running", name, "Middleware")
      try:
        result = self._middleware[name](components)

        if type(result) is not KiCadComponentList:
          Logger.Error("Middleware", name, "returned", type(result), "not KiCadComponentList--Restoring copy of components")
          return cpy

        return result

      except Exception as e:
        Logger.Error("Exception", e, "in", name, "Middleware--Restoring copy of components")
        return cpy

    return dispatchWrapper
