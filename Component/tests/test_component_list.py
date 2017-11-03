from __future__ import absolute_import

from Component import *

def test_adding_single_component():
  """ Tests adding a single component to a list """
  # Arrange
  component_list = KiCadComponentList()

  component = KiCadComponent({
    "name": "TestComponent"
  })

  # Act
  component_list.Add(component)

  # Assert
  assert len(component_list) == 1
  assert component_list[0] == component


def test_add_order():
  """ Tests maintaining the order of adding components """
  # Arrange
  component1 = KiCadComponent({
    "name": "TestComponent1"
  })
  component2 = KiCadComponent({
    "name": "TestComponent2"
  })

  expected = [component1, component2]

  # Act
  actual = KiCadComponentList()
  actual.Add(component1)
  actual.Add(component2)

  # Assert
  assert len(actual) == len(expected)

  for i in range(0, len(actual)):
    assert actual[i] == expected[i]


def test_delete():
  """ Tests removing an item """
  # Arrange
  component1 = KiCadComponent({
    "name": "TestComponent1"
  })
  component2 = KiCadComponent({
    "name": "TestComponent2"
  })
  component3 = KiCadComponent({
    "name": "TestComponent3"
  })

  expected = [component1, component3]

  # Act
  actual = KiCadComponentList()
  actual.Add(component1)
  actual.Add(component2)
  actual.Add(component3)

  del actual[1]

  # Assert
  assert len(actual) == len(expected)

  for i in range(0, len(actual)):
    assert actual[i] == expected[i]


def test_remove_with_component():
  """ Tests removing an item """
  # Arrange
  component1 = KiCadComponent({
    "name": "TestComponent1"
  })
  component2 = KiCadComponent({
    "name": "TestComponent2"
  })
  component3 = KiCadComponent({
    "name": "TestComponent3"
  })

  expected = [component1, component3]

  # Act
  actual = KiCadComponentList()
  actual.Add(component1)
  actual.Add(component2)
  actual.Add(component3)

  actual.Remove(component2)

  # Assert
  assert len(actual) == len(expected)

  for i in range(0, len(actual)):
    assert actual[i] == expected[i]


def test_remove_with_hash():
  """ Tests removing an item with a hash """
  # Arrange
  component1 = KiCadComponent({
    "name": "TestComponent1"
  })
  component2 = KiCadComponent({
    "name": "TestComponent2"
  })
  component3 = KiCadComponent({
    "name": "TestComponent3"
  })

  expected = [component1, component3]

  # Act
  actual = KiCadComponentList()
  actual.Add(component1)
  actual.Add(component2)
  actual.Add(component3)

  actual.Remove(component2.Hash())

  # Assert
  assert len(actual) == len(expected)

  for i in range(0, len(actual)):
    assert actual[i] == expected[i]


def test_remove_with_index():
  """ Tests removing an item using index """
  # Arrange
  component1 = KiCadComponent({
    "name": "TestComponent1"
  })
  component2 = KiCadComponent({
    "name": "TestComponent2"
  })
  component3 = KiCadComponent({
    "name": "TestComponent3"
  })

  expected = [component1, component3]

  # Act
  actual = KiCadComponentList()
  actual.Add(component1)
  actual.Add(component2)
  actual.Add(component3)

  actual.Remove(1)

  # Assert
  assert len(actual) == len(expected)

  for i in range(0, len(actual)):
    assert actual[i] == expected[i]


def test_iterator():
  """ Tests iterating over the list """
  # Arrange
  component1 = KiCadComponent({
    "name": "TestComponent1"
  })
  component2 = KiCadComponent({
    "name": "TestComponent2"
  })
  component3 = KiCadComponent({
    "name": "TestComponent3"
  })

  # Act
  actual = KiCadComponentList()
  actual.Add(component1)
  actual.Add(component2)
  actual.Add(component3)

  # Assert
  for c in actual:
    assert type(c) is KiCadComponent


def test_constructor():
  """ Test passing a list to the kicad component list """
  # Arrange
  expected = [
    KiCadComponent({
      "name": "TestComponent1"
    }),
    KiCadComponent({
      "name": "TestComponent2"
    }),
     KiCadComponent({
      "name": "TestComponent3"
    })
  ]

  # Act
  actual = KiCadComponentList(expected)

  # Assert
  assert len(actual) == len(expected)

  for i in range(0, len(actual)):
    assert actual[i] == expected[i]

