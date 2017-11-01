from Singleton import *


@Singleton
class MiddlewareRegistrar:
  """ A class used to register Middleware and dispatch Middleware """
  def __init__(self):
    self._middleware = {} # Start with nothing registered


  def Register(self, name, fn):
    """ Registers some middleware """
    print("Registering " + name.lower())
    self._middleware[name.lower()] = fn


  def Dispatch(self, name):
    """ Returns a function to wrap around middleware """
    name = name.lower()

    if name not in self._middleware:
      return None

    def dispatchWrapper(components):
      """ Wrapper Function to apply middleware """
      return self._middleware[name](components)

    return dispatchWrapper
