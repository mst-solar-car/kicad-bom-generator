__all__ = ['Get']

from .configuration import Configuration


def Get():
  """ Function to return configuration """
  return Configuration()