__all__ = ['Pipeline', 'Register', 'Apply']

import Config
import Logger
from .middleware_registrar import MiddlewareRegistrar

cfg = Config.Get()
registrar = MiddlewareRegistrar()


def Register(name):
  """ Decorator for Registering Middleware """
  def wrapper(middlewareFn):
    registrar.Register(name, middlewareFn)
    return middlewareFn

  return wrapper


def Pipeline(nextInPipeline):
  """ Decorator for using middleware in a pipeline (not the middleware pipeline) """
  def wrapper(components):
    return nextInPipeline(Apply(components))

  return wrapper


def Apply(components):
  """ Applies middleware to a list of components """
  for middleware in cfg['middleware']:
      middlewareFn = registrar.Dispatch(middleware)

      if middlewareFn is None:
        Logger.Error("Unkown Middleware", middleware)
        continue

      # Apply the middleware
      components = middlewareFn(components)

  return components
