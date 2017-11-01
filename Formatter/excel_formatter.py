import os

import Arguments
import Formatter
import Config

from openpyxl import Workbook

args = Arguments.Parse()
cfg = Config.Get()

@Formatter.Register("excel")
def excel_formatter(components):
  """ Formats a list of components into an excel spreadsheet """
  columns = cfg['columns']

  wb = Workbook()
  ws = wb.active

  # Add header row
  ws.append([c.replace('-', ' ').title() for c in columns])

  # Add a row for all the components
  for component in components:
    row = []

    for column in columns:
      try:
        row.append(str(component[column]))
      except:
        row.append("[error]")

    ws.append(row)

  # Save the excel file
  save_path = "{0}BOM.xlsx".format(args.project_folder)
  wb.save(save_path)

  return "BOM saved to \"{0}\"".format(save_path)
