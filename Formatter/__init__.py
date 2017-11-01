__all__ = ['Apply', 'Register']

import sys
import Arguments
import Middleware

from format_registrar import FormatRegistrar

args = Arguments.Parse()
registrar = FormatRegistrar()

def Apply(components):
  """ Apply the appropriate formatter to the list of components """
  fn = registrar.Dispatch(args.formatter)

  if fn is None:

  if fn is None:
    print("ERROR")
    sys.exit(0)

  # Wrap the formatter in middleware and stuff
  formatter = formatWrap(fn)

  return formatter(components)


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
