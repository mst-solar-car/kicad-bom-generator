import sys
import os
import fnmatch

import Arguments
import Formatter
import Parser
import Config

def getSchematicsFromFolder(dir):
  """ Finds all the .sch files in directory """
  files = []
  for root, dirnames, filenames in os.walk(dir):
    for file in filenames:
      if fnmatch.fnmatch(file, "*.sch"):
        files.append(root + file)

  return files

def main():
  """ Main """
  args = Arguments.Parse()
  cfg = Config.Get()

  # Find all the schematic files
  schematics = getSchematicsFromFolder(args.project_folder)

  # Parse components
  components = Parser.GetComponentsFromFiles(schematics)

  Formatter.Apply(components)