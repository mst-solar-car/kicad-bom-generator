__all__ = ['Parse']

import sys
from .argument_parser import ArgumentParser

def Parse(args = sys.argv[1:]):
  """ Little function to help with syntax """
  return ArgumentParser(args)