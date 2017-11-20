import os

import Arguments
import Formatter
import Config
import Logger
from Utils import *

import xlsxwriter

args = Arguments.Parse()
cfg = Config.Get()

@Formatter.Register("excel")
def excel_formatter(components):
  """ Formats a list of components into an excel spreadsheet """
  save_path = "{0}.xlsx".format(args.output_file)

  workbook = xlsxwriter.Workbook(save_path)
  ws = workbook.add_worksheet('BOM')

  # Create styling for the header titles
  header_style = workbook.add_format({
    'font_size': 16,
    'bold': True,
    'align': 'center',
    'bottom': 2,
    'right': 1,
  })

  # Create styling for general row
  row_style = workbook.add_format({
    'right': 1,
    'bottom': 1
  })

  columns = cfg['columns'] # List of columns

  # Add the columns to the file
  for col in range(0, len(columns)):
    ws.write(0, col, denormalizeStr(columns[col]), header_style)

  # Add a row for each component
  for row in range(0, len(components)):
    for col in range(0, len(columns)):
      try:
        ws.write(row + 1, col, components[row][columns[col]], row_style)
      except:
        ws.write(row + 1, col, cfg['emptyValue'], row_style)

  # Close the file
  workbook.close()

  return save_path

