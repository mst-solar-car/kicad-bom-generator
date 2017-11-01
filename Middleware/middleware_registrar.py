from Singleton import *


@Singleton
class MiddlewareRegistrar:
  """ A class used to register Middleware and dispatch Middleware """
  def __init__(self):
    self._middleware = {} # Start with nothing registered

  def normalize(self, s):
    return s.lower()

  def Register(self, name, fn):
    """ Registers some middleware """
    self._middleware[self.normalize(name)] = fn

  def Dispatch(self, name):
    """ Returns a function to wrap around middleware """
    name = self.normalize(name)

    if name not in self._middleware:
      return None

    def dispatchWrapper(components):
      """ Wrapper Function to apply middleware """
      return self._middleware[name](components)

    return dispatchWrapper
