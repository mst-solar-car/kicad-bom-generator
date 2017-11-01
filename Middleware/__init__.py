__all__ = ['Wrapper', 'Register']

import Config
from middleware_registrar import MiddlewareRegistrar

cfg = Config.Get()
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
    for middleware in cfg['defaults']['middleware']:
      middlewareFn = registrar.Dispatch(middleware)

      if middlewareFn is None:
        print("Unkown Middleware {0}".format(middleware))
        continue

      # Apply the middleware
      components = middlewareFn(components)

    # Run the components through the wrapped function and return the value
    return fn(components)

  return wrapper
