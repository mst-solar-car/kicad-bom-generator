__all__ = ['GetFormatter', 'Register']

import sys
import Arguments
import Middleware

from format_registrar import FormatRegistrar

args = Arguments.Parse()
registrar = FormatRegistrar()

def GetFormatter():
  """ Returns a function that can be used to format a list of components """
  formatter = args.formatter

  fn = registrar.Dispatch(formatter)

  if fn is None:
    print("ERROR")
    sys.exit(0)

  return formatWrap(fn)


def Register(name):
  """ Decorator for registering a formatter """
  def wrapper(formatterFn):
    registrar.Register(name, formatterFn)
    return formatterFn

  return wrapper


def formatWrap(fn):
  """ Wraps a function for formatting -- also applies middleware """
  @Middleware.Wrapper
  def wrapper(components):
    output = fn(components)
    # TODO: Save output
    return output

  return wrapper
