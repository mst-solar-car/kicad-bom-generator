from __future__ import absolute_import

from Component import *
from Middleware.sort_middleware import sort_middleware

components = KiCadComponentList([
  KiCadComponent({
    "name": "Component 1",
    "reference": "B1"
  }),
  KiCadComponent({
    "name": "Component 2",
    "reference": "A1"
  }),
  KiCadComponent({
    "name": "Component 3",
    "reference": "A2, A3, A4"
  }),
  KiCadComponent({
    "name": "Component 4",
    "reference": "D"
  }),
  KiCadComponent({
    "name": "Component 5",
    "reference": "B0"
  })
])

def test_sort_middleware():
  """ Test for the sort middleware """
  # Arrange
  expected = KiCadComponentList([
    KiCadComponent({
      "name": "Component 2",
      "reference": "A1"
    }),
    KiCadComponent({
      "name": "Component 3",
      "reference": "A2, A3, A4"
    }),
    KiCadComponent({
      "name": "Component 5",
      "reference": "B0"
    }),
    KiCadComponent({
      "name": "Component 1",
      "reference": "B1"
    }),
    KiCadComponent({
      "name": "Component 4",
      "reference": "D"
    })
  ])

  # Act
  result = sort_middleware(components)

  # Assert
  assert len(result) == len(expected)

  for i in range(0, len(result)):
    assert result[i] == expected[i]
