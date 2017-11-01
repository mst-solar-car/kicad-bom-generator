__all__ = ['GetComponentsFromFiles']

import re
from threading import Thread
from copy import deepcopy

import Config

cfg = Config.Get()

def GetComponentsFromFiles(files):
  """ Searches a list of files for components """
  thread_list = [] # List of threads

  component_list = [] # List of components

  # Start a new thread for every file in the list
  for file in files[:1]:
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
  parser = getComponentParser()

  for line in getLine(file):
    component = parser(line)

    if component is not None:
      component_list.append(component)



def getComponentParser():
  """
  Returns a closure for parsing a component line by line
  This should return None until a component is fully parsed, then it should return the component
  """
  def parser(line):
    """ Parse a component line by line """
    # Line "$Comp" signifies the start of a component definition
    if line == "$Comp":
      parser.component = {} # Create component object (just a dictionary)
      return None

    # The line "$EndComp" signifies the end of a component definition
    if line == "$EndComp" and parser.component is not None:
      parser.component['quantity'] = 1
      cpy = deepcopy(parser.component)
      parser.component = None
      return cpy

    # If the line is not "$Comp", and not "$EndComp" but component is None, then
    # We are not reading a line that defines a component
    if parser.component is None:
      return None


    # Now we are reading a line that defines a component
    # Break the line up into segments and go to town
    parts = line.split(' ') # Split at spaces

    # HOPEFULLY there are are always more than 3 parts to these component definition lines
    if len(parts) < 3:
      parser.component = None
      return None

    spec = parts[0][:1].upper()

    # L name reference
    if spec == "L":
      parser.component['name'] = parts[1].replace('"', '')
      parser.component['reference'] = [parts[2].replace('"', '')]

    # F num "value"
    elif spec == "F":
      num = int(parts[1])
      value = parts[2].replace('"', '')

      # F 1 "component-value"
      if num == 1:
        parser.component['value'] = value

      # F 2 "component-footprint"
      elif num == 2:
        parser.component['footprint'] = value

      # F 3 "datasheet"
      elif num == 3:
        parser.component['datasheet'] = value

      # F >3 "value" bunch of junk "name"
      elif num >= 3:
        matches = re.match(r'F (?:[0-9]*) "([^"]*)" (?:.*?) "([^["]*)"', line, re.M|re.I)

        if matches:
          name = matches.group(2).lower().replace(' ', '-')
          value = matches.group(1)

          # Alias lookup
          if name in cfg['metadataAliases']:
            name = cfg['metadataAliases'][name]

          parser.component[name] = value

    # Unkown spec (do nothing?)
    else:
      pass

    return None

  # Give the parser function a variable to keep track of the component
  parser.component = None

  return parser



def combineQuantities(components):
  """ Runs through a list of components and combines quantities for similar components """
  final = []

  def combineWithOthers(component, startIndex):
    if startIndex >= len(components):
      return component

    # Loop through components
    for i in range(startIndex, len(components)):
      comp = components[i]

      # Combine if they are the same component
      if componentsAreEqual(comp, component):
        component['quantity'] = component['quantity'] + comp['quantity']
        component['reference'] = component['reference'] + comp['reference']
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
