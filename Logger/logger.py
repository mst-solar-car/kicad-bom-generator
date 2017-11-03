import sys

from Singleton import *

def assembleMsg(*args):
  msg = ""
  for arg in args:
    msg = msg + str(arg) + " "
  return msg


@Singleton
class Logger:
  """ Class for logging """
  def __init__(self):
    self.verbose = False
    self.debug = False

  def Log(self, *args):
    """ A simple regular log message """
    print(assembleMsg(*args))

  def Verbose(self, *args):
    """ A Verbose log message """
    if not self.verbose:
      return

    print("V: {0}".format(assembleMsg(*args)))

  def Debug(self, *args):
    """ A debug message """
    if not self.debug:
      return

    print("D: {0}".format(assembleMsg(*args)))

  def Error(self, *args):
    """ An error message """
    print("E: {0}".format(assembleMsg(*args)))

  def Fatal(self, *args):
    """ A fatal message (exit the program) """
    print("\nFatal Error: {0}\n".format(assembleMsg(*args)))
    sys.exit(-1)
