
def normalizeStr(input):
  """ Normalizes the style of input """
  try:
    return str(input).lower().strip().replace(' ', '_')
  except:
    return input

def denormalizeStr(input):
  """ Denormalizes a string """
  try:
    return str(input).replace('_', ' ').title().strip()
  except:
    return input