import sys
import os
import fnmatch

import Arguments
import Formatters
import Parser

#args = sys.argv[1:]

# Friendlier names for arguments
#xml_file = args[0]
#project_folder = args[1]

#os.remove(xml_file) # Remove the XML file since we won't be needing it


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

  schematics = getSchematicsFromFolder(args.project_folder)

  Parser.GetComponentsFromFiles(schematics)