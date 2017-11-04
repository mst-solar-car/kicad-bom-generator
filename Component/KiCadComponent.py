from copy import deepcopy

class KiCadComponent(object):
  """ Class that will represent a KiCad Component """
  def __init__(self, dictData=None, **kwargs):
    # Dictionary of data
    self.data = {
      "name": "",
      "footprint": "",
      "reference": "",
      "value": "",
      "quantity": 1
    }

    # Allow ititialization with a dictionary
    if type(dictData) is dict:
      for key in dictData:
        self.data[key] = dictData[key]

  def Hash(self):
    """ Return a hash that is used to uniquely identify components """
    def norm(s):
      return s.lower().replace(' ', '_')

    name = norm(self.data["name"])
    footprint = norm(self.data["footprint"])
    value = norm(self.data["value"])

    return hash((name, footprint, value))

  def __hash__(self):
    """ Used to get a dictionary key """
    return self.Hash()

  def Copy(self):
    """ A copy function without copy module """
    return self.__copy__()

  def __copy__(self):
    """ Duplicates a component """
    cpy = KiCadComponent(deepcopy(self.data))
    return cpy

  def __deepcopy__(self, memo):
    """ Deep copy of a component """
    return self.__copy__()

  def __getitem__(self, key):
    """ Index Operator Part 1 """
    if key not in self.data:
      return None
    return self.data[key]

  def __setitem__(self, key, value):
    """ Index Operator Part 2 """
    self.data[key] = value

  def __eq__(self, other):
    """ Check if two components are equal """
    if type(other) is not KiCadComponent:
      return False
    return self.Hash() == other.Hash()

  def __ne__(self, other):
    """ check if two components are not equal """
    return not (self == other)

  def __str__(self):
    """ Convert to a string """
    return str(self.data)

  def __contains__(self, key):
    """ Determines if key is a valid attribute on the component """
    return key in self.data



