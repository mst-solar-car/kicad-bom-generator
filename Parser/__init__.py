__all__ = ['Pipeline', 'GetComponentsFromNetlist']

from .netlist_parser import *

def Pipeline(nextInPipeline):
  """ Decorator for using the parser in a pipeline fashion """
  def wrapper(netlist):
    return nextInPipeline(GetComponentsFromNetlist(netlist))

  return wrapper


