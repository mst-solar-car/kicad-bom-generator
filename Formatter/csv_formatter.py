import Formatter
import Config


cfg = Config.Get()


@Formatter.Register("csv")
def csv_formatter(components):
  """ Formats components as a CSV """
  columns = cfg['columns']
  nl = cfg['outputLineSeparator']

  result = columns[0].replace('-', ' ').title()

  # Add column headers
  for column in columns[1:]:
    result = result + "," + column.replace('-', ' ').title()

  # Add components
  for component in components:
    result = result + nl + str(component[columns[0]])

    for i in range(1, len(columns)):
      try:
        result = result + "," + str(component[columns[i]])
      except:
        result = result + ",[error]"

  return result