import Middleware



@Middleware.Register("test")
def test_middleware(components):
  print("In Test Middleware")
