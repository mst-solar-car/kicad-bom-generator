from __future__ import absolute_import

from Middleware.sort_middleware import sort_middleware

components = [
  {
    "name": "Component 1",
    "reference": "B1"
  },
  {
    "name": "Component 2",
    "reference": "A1"
  },
  {
    "name": "Component 3",
    "reference": "A2, A3, A4"
  },
  {
    "name": "Component 4",
    "reference": "D"
  },
  {
    "name": "Component 5",
    "reference": "B0"
  }
]

def test_sort_middleware():
  """ Test for the sort middleware """
  # Arrange
  expected = [
    {
      "name": "Component 2",
      "reference": "A1"
    },
    {
      "name": "Component 3",
      "reference": "A2, A3, A4"
    },
    {
      "name": "Component 5",
      "reference": "B0"
    },
    {
      "name": "Component 1",
      "reference": "B1"
    },
    {
      "name": "Component 4",
      "reference": "D"
    }
  ]

  # Act
  result = sort_middleware(components)

  # Assert
  for i in range(0, len(result)):
    assert result[i]["reference"] == expected[i]["reference"]
