__all__ = ['Wrapper', 'Register']

import Config
import Logger
from .middleware_registrar import MiddlewareRegistrar

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
    # Run through middleware pipeline
    for middleware in cfg['middleware']:
      middlewareFn = registrar.Dispatch(middleware)

      if middlewareFn is None:
        Logger.Error("Unkown Middleware", middleware)
        continue

      # Apply the middleware
      components = middlewareFn(components)

    # Run the components through the wrapped function and return the value
    return fn(components)

  return wrapper
