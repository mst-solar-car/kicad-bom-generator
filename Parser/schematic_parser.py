from threading import Thread
from copy import deepcopy

import Config

from Component import *

from .component_builder import ComponentBuilder

cfg = Config.Get()


def GetComponentsFromFiles(files):
  """ Searches a list of files for components """
  thread_list = [] # List of threads

  component_list = KiCadComponentList() # List of components

  # Start a new thread for every file in the list
  for file in files:
    t = Thread(target=fileParseThread, args=(file, component_list))
    t.start()
    thread_list.append(t)

  # Wait until all threads are finished
  for mythread in thread_list:
    mythread.join()

  # Return a component list with combined quantities
  return component_list


def fileParseThread(file, component_list):
  """ Function used as a thread to parse components from files """
  builder = ComponentBuilder()

  for line in getLine(file):
    component = builder.ParseLine(line)

    if component is not None:
      component_list.Add(component)


def getLine(file):
  """ Generator for getting each line of a file one at a time """
  f = open(file)

  for line in iter(f):
    yield line.strip()

  f.close()