from __future__ import absolute_import

from Component import *

import os
import Parser

# Folder for testing filess
folder = os.path.dirname(os.path.abspath(__file__)) + "/files"

single_simple_component = "{0}/single_simple_component.xml".format(folder) # File with only a single component in it
single_complex_component = "{0}/single_complex_component.xml".format(folder)
multiple_components = "{0}/multiple_components.xml".format(folder)
multiple_components_duplicates = "{0}/multiple_components_duplicates.xml".format(folder)


def test_parse_simple_component_single_file():
  """ Checks that parsing a single file with a single component in it works """
  # Arrange
  expected_component = KiCadComponent({
    "name": "SimpleComponent",
    "reference": "A3",
    "value": "SimpleComponent-Value",
    "footprint": "footprint-lib:footprint",
    "datasheet": "datasheet-url",
    "quantity": 1
  })

  # Act
  components_found = Parser.GetComponentsFromNetlist(single_simple_component)

  # Assert
  assert len(components_found) == 1
  assert components_found[0] == expected_component, str(components_found[0]) + " != " + str(expected_component)


def test_parse_complex_component_single_file():
  """ Checks that parsing a single file with a single component in it works """
  # Arrange
  expected_component = KiCadComponent({
    "name": "ComplexComponent",
    "reference": "A4",
    "value": "ComplexComponent-Value",
    "footprint": "footprint-lib:complex-footprint",
    "datasheet": "datasheet-url",
    "hopefully-this-is-not-an-alias": "Digikey",
    "hopefully-this-is-not-an-alias2": "666",
    "quantity": 1
  })

  # Act
  components_found = Parser.GetComponentsFromNetlist(single_complex_component)

  # Assert
  assert len(components_found) == 1
  assert components_found[0] == expected_component, str(components_found[0]) + " != " + str(expected_component)


def test_parse_multiple_components_single_file():
  """ Test that the parser can return multiple components from a single file accurately """
  # Arrange
  expected_components = KiCadComponentList([
    KiCadComponent({
      "name": "Component1",
      "reference": "A1",
      "value": "value1",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    }),
    KiCadComponent({
      "name": "Component2",
      "reference": "A2",
      "value": "value2",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    }),
    KiCadComponent({
      "name": "Component3",
      "reference": "A3",
      "value": "value3",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    })
  ])

  # Act
  components_found = Parser.GetComponentsFromNetlist(multiple_components)

  # Assert
  assert len(components_found) == len(expected_components)

  for i in range(0, len(components_found)):
    assert components_found[i] == expected_components[i], str(components_found[i]) + " != " + str(expected_components[i])


def test_parse_multiple_duplicate_components_single_file():
  """ Test that the parser can return multiple components (with duplicates) from a single file accurately """
  # Arrange
  expected_components = KiCadComponentList([
    KiCadComponent({
      "name": "Component1",
      "reference": "A4, A7",
      "value": "value1",
      "footprint": "footprint-lib:footprint",
      "quantity": 2
    }),
    KiCadComponent({
      "name": "Component2",
      "reference": "A5",
      "value": "value2",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    }),
    KiCadComponent({
      "name": "Component3",
      "reference": "A6",
      "value": "value3",
      "footprint": "footprint-lib:footprint",
      "quantity": 1
    })
  ])

  # Act
  components_found = Parser.GetComponentsFromNetlist(multiple_components_duplicates)

  # Assert
  assert len(components_found) == len(expected_components)

  for i in range(0, len(components_found)):
    assert components_found[i] == expected_components[i], str(components_found[i]) + " != " + str(expected_components[i])
