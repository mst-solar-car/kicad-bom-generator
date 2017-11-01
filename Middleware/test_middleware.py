import Middleware



@Middleware.Register("Meow")
def test_middleware(components):
  print("meow")


print("test middleware")