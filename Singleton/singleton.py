class Singleton:
  def __init__(self, decorated):
    self._decorated = decorated
    self._instance = None

  def __call__(self):
    """ Return the singleton instance """
    if self._instance is None:
      self._instance = self._decorated()

    return self._instance


