__all__ = ['Wrapper', 'Register']

from middleware_registrar import MiddlewareRegistrar


registrar = MiddlewareRegistrar()


def Register(name):
  """ Decorator for Registering Middleware """
  def wrapper(middlewareFn):
    registrar.Register(name, middlewareFn)

    return registrar.Dispatch(name)

  return wrapper


def Wrapper(fn):
  """ Middleware wrapper for a component list """
  def wrapper(components):
    components = applyMiddleware(components)

    return fn(components)

  return wrapper




@Register('boobs')
def testMiddleware(components):
  print("Howdy")