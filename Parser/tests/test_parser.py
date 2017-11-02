from __future__ import absolute_import

import os
import Parser

# Folder for testing filess
folder = os.path.dirname(os.path.abspath(__file__)) + "/files"

single_simple_component = "{0}/single_simple_component.sch".format(folder) # File with only a single component in it
single_complex_component = "{0}/single_complex_component.sch".format(folder)
multiple_components = "{0}/multiple_components.sch".format(folder)
multiple_components_duplicates = "{0}/multiple_components_duplicates.sch".format(folder)


def components_equal(actual, expected):
  """ Used for confirming that two components are exactly the same """
  for key in actual:
    if key not in expected:
      return False # Key is missing

    if expected[key] != actual[key]:
      return False # Values are differen t

  return True # Components are the same


def test_parse_simple_component_single_file():
  """ Checks that parsing a single file with a single component in it works """
  # Arrange
  expected_component = {
    "name": "SimpleComponent",
    "reference": "A3",
    "value": "SimpleComponent-Value",
    "footprint": "footprint-lib:footprint",
    "datasheet": "datasheet-url",
    "quantity": 1
  }

  # Act
  components_found = Parser.GetComponentsFromFiles([single_simple_component])

  # Assert
  assert len(components_found) == 1
  assert components_equal(components_found[0], expected_component), str(components_found[0]) + " != " + str(expected_component)


def test_parse_complex_component_single_file():
  """ Checks that parsing a single file with a single component in it works """
  # Arrange
  expected_component = {
    "name": "ComplexComponent",
    "reference": "A4",
    "value": "ComplexComponent-Value",
    "footprint": "footprint-lib:complex-footprint",
    "datasheet": "datasheet-url",
    "hopefully-this-is-not-an-alias": "Digikey",
    "hopefully-this-is-not-an-alias2": "666",
    "quantity": 1
  }

  # Act
  components_found = Parser.GetComponentsFromFiles([single_complex_component])

  # Assert
  assert len(components_found) == 1
  assert components_equal(components_found[0], expected_component), str(components_found[0]) + " != " + str(expected_component)



def test_parse_multiple_components_single_file():
  """ Test that the parser can return multiple components from a single file accurately """
  # Arrange
  expected_components = [
    {
      "name": "Component1",
      "reference": "A1",
      "value": "value1",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    },
    {
      "name": "Component2",
      "reference": "A2",
      "value": "value2",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    },
    {
      "name": "Component3",
      "reference": "A3",
      "value": "value3",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    }
  ]

  # Act
  components_found = Parser.GetComponentsFromFiles([multiple_components])

  # Assert
  assert len(components_found) == len(expected_components)

  for i in range(0, len(components_found)):
    assert components_equal(components_found[i], expected_components[i]), str(components_found[i]) + " != " + str(expected_components[i])


def test_parse_multiple_duplicate_components_single_file():
  """ Test that the parser can return multiple components (with duplicates) from a single file accurately """
  # Arrange
  expected_components = [
    {
      "name": "Component1",
      "reference": "A4, A7",
      "value": "value1",
      "footprint": "footprint-lib:footprint",
      "quantity": 2
    },
    {
      "name": "Component2",
      "reference": "A5",
      "value": "value2",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    },
    {
      "name": "Component3",
      "reference": "A6",
      "value": "value3",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    }
  ]

  # Act
  components_found = Parser.GetComponentsFromFiles([multiple_components_duplicates])

  # Assert
  assert len(components_found) == len(expected_components)

  for i in range(0, len(components_found)):
    assert components_equal(components_found[i], expected_components[i]), str(components_found[i]) + " != " + str(expected_components[i])


def test_multiple_files():
  """ Tests that the parser can return multiple components (with duplicates) from multiple files """
  # Arrange
  expected_components = [
    {
      "name": "Component1",
      "reference": "A1, A4, A7",
      "value": "value1",
      "footprint": "footprint-lib:footprint",
      "quantity": 3
    },
    {
      "name": "Component2",
      "reference": "A2, A5",
      "value": "value2",
      "footprint": "footprint-lib:footprint",
      "quantity": 2
    },
    {
      "name": "Component3",
      "reference": "A3, A6",
      "value": "value3",
      "footprint": "footprint-lib:footprint",
      "quantity": 2
    }
  ]

  files = [multiple_components, multiple_components_duplicates]

  # Act
  components_found = Parser.GetComponentsFromFiles([multiple_components, multiple_components_duplicates])

  # Assert
  assert len(components_found) == len(expected_components)

  for i in range(0, len(components_found)):
    assert components_equal(components_found[i], expected_components[i]), str(components_found[i]) + " != " + str(expected_components[i])

