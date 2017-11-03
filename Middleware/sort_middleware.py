import Middleware
from Component import *

@Middleware.Register("sort")
def sort_middleware(components):
  """ Sorts the components by their reference """
  return KiCadComponentList(sorted(components, key=lambda c: c['reference']))