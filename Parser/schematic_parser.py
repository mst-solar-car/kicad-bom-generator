from threading import Thread
from copy import deepcopy

import Config

from .component_builder import ComponentBuilder

cfg = Config.Get()


def GetComponentsFromFiles(files):
  """ Searches a list of files for components """
  thread_list = [] # List of threads

  component_list = [] # List of components

  # Start a new thread for every file in the list
  for file in files:
    t = Thread(target=fileParseThread, args=(file, component_list))
    t.start()
    thread_list.append(t)

  # Wait until all threads are finished
  for mythread in thread_list:
    mythread.join()

  # Return a component list with combined quantities
  return combineQuantities(component_list)



def fileParseThread(file, component_list):
  """ Function used as a thread to parse components from files """
  builder = ComponentBuilder()

  for line in getLine(file):
    component = builder.ParseLine(line)

    if component is not None:
      component_list.append(component)



def combineQuantities(components):
  """ Runs through a list of components and combines quantities for similar components """
  final = []

  def combineWithOthers(component, startIndex):
    if startIndex >= len(components):
      return component

    # Loop through components
    for i in range(startIndex, len(components)):
      comp = components[i]
      if comp is None:
        continue
      # Combine if they are the same component
      if componentsAreEqual(comp, component):
        component['quantity'] = component['quantity'] + comp['quantity']
        component['reference'] = component['reference'] + ", " + comp['reference']
        components[i] = None

    return component

  # Loop through all components
  for i in range(0, len(components)):
    component = components[i]

    # Do not consider components that are None
    if component is None:
      continue

    # Combine with all the others
    component = combineWithOthers(component, i + 1)
    final.append(component)

  return final



def componentsAreEqual(c1, c2):
  """ Compare two components """
  return (c1['name'] == c2['name']) and (c1['footprint'] == c2['footprint']) and (c1['value'] == c2['value'])



def getLine(file):
  """ Generator for getting each line of a file one at a time """
  f = open(file)

  for line in iter(f):
    yield line.strip()

  f.close()