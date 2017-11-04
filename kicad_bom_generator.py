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

def main():
  """ Main """
  # Parse components
  components = Parser.GetComponentsFromNetlist(args.input_file)

  # Run through middleware and formatter
  Formatter.Apply(components)

  os.remove(args.input_file)


# Load Middleware
load_modules("Middleware")

# Load Formatters
load_modules("Formatter")

if __name__ == "__main__":
  main()