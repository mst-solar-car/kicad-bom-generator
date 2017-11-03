import threading
from copy import deepcopy
from .KiCadComponent import KiCadComponent


class KiCadComponentList:
  """ Class to represent a list of KiCadComponents """
  def __init__(self, data=None):
    self.components = {}
    self.order = [] # List of hashes representing the order of the components
    self._lock = threading.RLock()
    self.index = 0

    # Allow initialization
    if type(data) is list:
      for component in data:
        if type(component) is KiCadComponent:
          hash = component.Hash()
          self.order.append(hash)
          self.components[hash] = component.Copy()

  def Add(self, new_component):
    """ Add a component from the list """
    # Combine with an existing component
    self._lock.acquire()
    try:
      hash = new_component.Hash()

      if hash in self.components:
        # Update quantity and references of the component
        self.components[hash]["quantity"] = self.components[hash]["quantity"] + new_component["quantity"]
        self.components[hash]["reference"] = self.components[hash]["reference"] + ", " + new_component["reference"]
      else:
        self.components[hash] = deepcopy(new_component)
        self.order.append(hash)

    except:
      pass
    self._lock.release()

  def Remove(self, value):
    """ Removes a component from the list """
    self._lock.acquire()
    try:
      hash = None
      index = None

      if type(value) is int:
        # Check if hash
        if value in self.components:
          hash = value
          for i in range(0, len(self.order)):
            if self.order[i] == hash:
              index = i
              break
        elif value < len(self.order) and value >= 0:
          # Standard index
          index = value
          hash = self.order[index]

      elif type(value) is KiCadComponent:
        # Value is a component
        self._lock.release()
        return self.Remove(value.Hash()) # Remove using the hash
      else:
        # Not found
        raise KeyError()

      # Remove the item
      del self.components[hash]
      del self.order[index]
    except:
      pass
    self._lock.release()

  def __getitem__(self, index):
    """ Index Operator """
    if index in self.components:
      return self.components[index]
    elif index < len(self.order):
      key = self.order[index]
      if key in self.components:
        return self.components[key]
    return None

  def __delitem__(self, key):
    """ Removes an item from the list """
    self._lock.acquire()
    try:
      hash = None
      index = None

      if key < len(self.order) and key >= 0:
        # Key is an index
        hash = self.order[key]
        index = key
      else:
        # Invalid key
        self._lock.release()
        raise KeyError()

      del self.components[hash] # Remove from dictionary
      del self.order[index]
    except:
      pass

    self._lock.release() # release before leaving method

  def __len__(self):
    """ Get the number of unique components """
    return len(self.components)

  def __iter__(self):
    """ Make this class iterable """
    self.index = 0
    return self

  def __next__(self):
    """ Python 3 iteration """
    self.index = self.index + 1
    if self.index >= len(self.order):
      raise StopIteration

    return self.components[self.order[self.index]]

  def next(self):
    """ Python <3 iteration """
    return self.__next__()

