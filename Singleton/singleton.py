class Singleton:
  def __init__(self, decorated):
    self._decorated = decorated
    self._instance = None


  def __call__(self, *args, **kwargs):
    """ Return the singleton instance """
    if self._instance is None:
      self._instance = self._decorated(*args, **kwargs)

    return self._instance

  def Reset(self):
    """ Clears a singleton object, only used in tests """
    self._instance = None


