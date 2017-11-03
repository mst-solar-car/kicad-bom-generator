import sys
import os
import glob
import importlib
import fnmatch

import Arguments
import Formatter
import Parser
import Config
import Logger

# Parse command line arguments and get configuration
args = Arguments.Parse()

# Path that the script is in
script_dir = os.path.dirname(os.path.realpath(__file__))

def load_modules(module_folder):
  """ Loads all custom modules from a module folder """
  found = glob.glob(script_dir + '/' + module_folder + '/*_' + module_folder.lower() + '.py')

  for file in found:
    name = os.path.basename(file).replace('.py', '') # Remove file extension
    module = "{0}.{1}".format(module_folder, name)

    Logger.Debug("Importing: {0}".format(module))
    importlib.import_module(module)

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
  # Find all the schematic files
  schematics = getSchematicsFromFolder(args.project_folder)

  # Parse components
  components = Parser.GetComponentsFromFiles(schematics)

  # Run through middleware and formatter
  Formatter.Apply(components)


# Load Middleware
load_modules("Middleware")

# Load Formatters
load_modules("Formatter")

if __name__ == "__main__":
  main()