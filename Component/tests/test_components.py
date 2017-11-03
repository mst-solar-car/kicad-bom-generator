from __future__ import absolute_import

from Component import *

def test_default_values():
  """ Tests the initial constructor values """
  # Arrange
  expected_name = ""
  expected_footprint = ""
  expected_reference = ""
  expected_value = ""
  expected_quantity = 1

  # Act
  component = KiCadComponent()

  # Assert
  assert component["name"] == expected_name
  assert component["footprint"] == expected_footprint
  assert component["reference"] == expected_reference
  assert component["value"] == expected_value
  assert component["quantity"] == expected_quantity


def test_constructor():
  """ Tests the constructor, and index operator """
  # Arrange
  expected_name = "TestComponent"
  expected_value = "TestValue"
  expected_footprint = "TestFootprint"

  # Act
  actual = KiCadComponent({
    "name": expected_name,
    "value": expected_value,
    "footprint": expected_footprint
  })

  # Assert
  assert actual["name"] == expected_name
  assert actual["value"] == expected_value
  assert actual["footprint"] == expected_footprint


def test_comparions():
  """
  Tests that two components with the same name, footprint, and value are equal
  And that one with different values will be different
  """
  # Arrange
  name = "TestComponent"
  value = "TestValue"
  footprint = "TestFootprint"

  # Act
  component1 = KiCadComponent({
    "name": name,
    "value": value,
    "footprint": footprint,
    "datasheet": "different value",
    "quantity": 10
  })

  component2 = KiCadComponent({
    "name": name,
    "value": value,
    "footprint": footprint,
    "quantity": 5
  })

  component3 = KiCadComponent({
    "name": name,
    "value": value[:-1],
    "footprint": footprint,
    "datasheet": "different value",
    "quantity": 10
  })

  # Assert
  assert component1 == component2
  assert component1 != component3
  assert component2 != component3


def test_setting_values():
  """ Tests that you can set values on a component """
  # Arrange
  expected_name = "TestComponent"
  expected_value = "TestValue"

  # Act
  component = KiCadComponent()
  component["name"] = expected_name
  component["value"] = expected_value

  # Assert
  assert component["name"] == expected_name
  assert component["value"] == expected_value

def test_copy():
  """ Tests the copy function """
  # Arrange
  expected_name = "TestComponent"
  expected_value = "TestValue"

  component = KiCadComponent({
    "name": expected_name,
    "value": expected_value
  })

  # Act
  new_component = component.Copy()

  component["name"] = "Component"
  component["value"] = "Value"

  # Assert
  assert new_component["name"] == expected_name
  assert new_component["value"] == expected_value
