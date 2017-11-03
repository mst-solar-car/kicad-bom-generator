import json

import Formatter
import Config

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

  return json.dumps(newList)