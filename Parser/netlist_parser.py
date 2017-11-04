from copy import deepcopy

import xml.etree.ElementTree as ET

import Config
import Logger
from Component import *

cfg = Config.Get()


def GetComponentsFromNetlist(netlist):
  """ Reads a netlist file and extracts components """
  component_list = KiCadComponentList() # List of components

  tree = ET.parse(netlist)

  # Tree traversal
  root = tree.getroot()
  for item in root:
    if item.tag == "components":
      # Parse components
      for component in item:
        if component.tag == "comp":
          c = buildComponent(component)
          if c is not None:
            component_list.Add(c)
      break

  return component_list


def buildComponent(component_tree):
  """ Builds a component from the tree """
  component = KiCadComponent()

  component[getAlias('reference')] = component_tree.attrib['ref']

  for prop in component_tree:
    if prop.tag == "fields":
      # Handle custom fields
      for field in prop:
        component[getAlias(field.attrib['name'])] = field.text
    elif prop.tag == "libsource":
      # Set library source and name
      component[getAlias('library')] = prop.attrib['lib']
      component[getAlias('name')] = prop.attrib['part']
    elif prop.tag == "sheetpath":
      # Sheet path
      component[getAlias('sheet')] = prop.attrib['names']
    else:
      # Regular field
      component[getAlias(prop.tag)] = prop.text

  return component

def getAlias(name):
  """ Returns any aliases """
  name = name.lower().replace(' ', '_')
  if name in cfg['metadataAliases']:
    return cfg['metadataAliases'][name] # ALias found

  return name

def getLine(file):
  """ Generator for getting each line of a file one at a time """
  f = open(file)

  for line in iter(f):
    yield line.strip()

  f.close()
