from __future__ import absolute_import

import Middleware
from Middleware.middleware_registrar import MiddlewareRegistrar

@Middleware.Register("middleware-registration-unit-test")
def test_middleware(components):
  """ Test middleware function that returns a simple number """
  return 5


def test_middleware():
  """ Confirms that the above middleware was register """
  # Arrange
  registrar = MiddlewareRegistrar()
  middleware = registrar.Dispatch("middleware-registration-unit-test") # Get the function that the middleware is registered as
  expected = 5

  # Act
  actual = middleware(6) # Run the number 6 through our middleware

  # Assert
  assert actual == expected
