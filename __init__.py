import os
import glob
import importlib

import kicad_bom_generator

# Path that the script is in
script_dir = os.path.dirname(os.path.realpath(__file__))


def load_modules(module_folder):
  """ Loads all custom modules from a module folder """
  found = glob.glob(script_dir + '/' + module_folder + '/*_' + module_folder.lower() + '.py')

  for file in found:
    name = os.path.basename(file).replace('.py', '') # Remove file extension
    importlib.import_module(module_folder + '.' + name)


# Load Middleware
load_modules("Middleware")

# Load Formatters
load_modules("Formatters")

# Start doing actual things
kicad_bom_generator.main()