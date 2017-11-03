"""
This file contains a class that will build a component line by line based on the
following spec:
http://bazaar.launchpad.net/~stambaughw/kicad/doc-read-only/download/head:/1115%4016bec504-3128-0410-b3e8-8e38c2123bca:trunk%252Fkicad-doc%252Fdoc%252Fhelp%252Ffile_formats%252Ffile_formats.pdf/file_formats.pdf
"""
from copy import deepcopy

import re
import Config

from Component import KiCadComponent

cfg = Config.Get()



class ComponentBuilder:
  """ Class that is used to build components from a .sch file line by line """
  def __init__(self):
    self.component = None

  def ParseLine(self, line):
    """ Method used to parse a single line of a .sch file """
    # The Line "$Comp" signifies the start of a component definition
    if line == "$Comp":
      self.component = KiCadComponent()
      return None

    # The line "$EndComp" signifies the end of a component definition
    if line == "$EndComp" and self.component is not None:
      # Return a copy of the built component
      cpy = self.component.Copy()
      self.component = None

      return cpy

    # At this point, if self.component is None then we are reading a line that is not important
    if self.component is None:
      return None

    # Now we are reading a line that defines a component
    # Break the line up into segments and go to town
    parts = line.split(' ') # Split at spaces

    # HOPEFULLY there are are always more than 3 parts to these component definition lines
    if len(parts) < 3:
      self.component = None
      return None

    spec = parts[0][:1].upper()

    # L name reference
    if spec == "L":
      self.component['name'] = parts[1].replace('"', '')
      self.component['reference'] = parts[2].replace('"', '')

    # F num "value"
    elif spec == "F":
      num = int(parts[1])
      value = parts[2].replace('"', '')

      # F 1 "component-value"
      if num == 1:
        self.component['value'] = value

      # F 2 "component-footprint"
      elif num == 2:
        self.component['footprint'] = value

      # F 3 "datasheet"
      elif num == 3:
        self.component['datasheet'] = value

      # F >3 "value" bunch of junk "name"
      elif num >= 3:
        matches = re.match(r'F (?:[0-9]*) "([^"]*)" (?:.*?) "([^["]*)"', line, re.M|re.I)

        if matches:
          name = matches.group(2).lower().replace(' ', '-')
          value = matches.group(1)

          # Alias lookup
          if name in cfg['metadataAliases']:
            name = cfg['metadataAliases'][name]

          self.component[name] = value

    # Unkown spec (do nothing?)
    else:
      pass


    return None # Not finished yet


