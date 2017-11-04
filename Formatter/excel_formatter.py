import os

import Arguments
import Formatter
import Config
from Utils import *

from openpyxl import Workbook
from openpyxl.styles import Alignment

args = Arguments.Parse()
cfg = Config.Get()

@Formatter.Register("excel")
def excel_formatter(components):
  """ Formats a list of components into an excel spreadsheet """
  columns = cfg['columns']

  wb = Workbook()
  ws = wb.active

  # Add header row
  ws.append([denormalizeStr(c) for c in columns])

  # Format the header cells
  for cell in ws._cells_by_col(1, 1, len(columns), 1):
    cell[0].style= 'Headline 1'
    cell[0].alignment = Alignment(horizontal='center')

  # Add a row for all the components
  for component in components:
    row = []

    for column in columns:
      try:
        row.append(component[column])
      except:
        row.append(cfg['emptyValue'])

    ws.append(row)

  # Save the excel file
  save_path = "{0}.xlsx".format(args.output_file)
  wb.save(save_path)

  return "BOM saved to \"{0}\"".format(save_path)
