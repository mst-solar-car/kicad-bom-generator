import Middleware



@Middleware.Register("test")
def test_middleware(components):
  return components
