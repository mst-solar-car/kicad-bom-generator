import json

import Formatter
import Config
import Arguments
import Logger

args = Arguments.Parse()
cfg = Config.Get()


@Formatter.Register("json")
def json_formatter(components):
  """ Formats the component list as JSON """
  columns = cfg['columns']

  newList = [] # New list of only dictionaries with column attributes to marshall

  for component in components:
    newComp = {}

    for column in columns:
      try:
        newComp[column] = component[column]
      except:
        newComp[column] = cfg['emptyValue']

    newList.append(newComp)

  result = json.dumps(newList)

   # Save the json file
  save_path = "{0}.json".format(args.output_file)
  try:
    with open(save_path, "w") as file:
      file.write(result)

    Logger.Debug("Output saved to", save_path)

    return "BOM saved to \"{0}\"".format(save_path)

  except:
    Logger.Error("Could not save output to", save_path)
