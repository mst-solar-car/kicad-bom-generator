import Formatter
import Config
import Logger
import Arguments

args = Arguments.Parse()
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
        result = result + "," + str(cfg['emptyValue'])

  # Save the csv file
  save_path = "{0}.csv".format(args.output_file)
  try:
    with open(save_path, "w") as file:
      file.write(result)

    Logger.Debug("Output saved to", save_path)
    return "BOM saved to \"{0}\"".format(save_path)

  except:
    Logger.Error("Could not save output to", save_path)
