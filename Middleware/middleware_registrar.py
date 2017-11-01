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
    if name not in self._middleware:
      print("UH OH")
      return None

    def dispatchWrapper(components):
      """ Wrapper Function to apply middleware """
      return self._middleware[name](components)

    return dispatchWrapper

  def __getitem__(self, name):
    """ Index Operator """
    if name in self._middleware:
      return self._middleware[name]
    else:
      return None


