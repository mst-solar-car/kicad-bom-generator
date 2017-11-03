from __future__ import absolute_import

import Middleware
from Component import *
from Middleware.middleware_registrar import MiddlewareRegistrar

@Middleware.Register("middleware-registration-unit-test")
def test_middleware(components):
  """ Test middleware function that returns a simple number """
  for component in components:
    component['quantity'] = component['quantity'] + 1

  return components


def test_middleware():
  """ Confirms that the above middleware was register """
  # Arrange
  registrar = MiddlewareRegistrar()
  middleware = registrar.Dispatch("middleware-registration-unit-test") # Get the function that the middleware is registered as
  expected = KiCadComponentList({
    "name": "TestComponent",
    "quantity": 11
  })

  # Act
  actual = middleware(KiCadComponentList({
    "name": "TestComponent",
    "quantity": 10
  }))

  # Assert
  assert len(actual) == len(expected)

  for i in range(0, len(actual)):
    assert actual[i] == expected[i]
