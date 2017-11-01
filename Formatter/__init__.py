__all__ = ['Apply', 'Register']

import sys
import Config
import Arguments
import Middleware

from format_registrar import FormatRegistrar

cfg = Config.Get()
args = Arguments.Parse()
registrar = FormatRegistrar()


@Middleware.Wrapper
def Apply(components):
  """ Apply the appropriate formatter to the list of components (after middleware) """
  formatter = registrar.Dispatch(args.formatter)

  if formatter is None:
    # Attempt to load formatter from config.json
    formatter = registrar.Dispatch(cfg['defaultFormatter'])

    if formatter is None:
      print("Error: Unkown Formatter {0}".format(args.formatter))
      sys.exit(0)

  # Run through the formatter
  output = formatter(components)

  print(output)

  return output


def Register(name):
  """ Decorator for registering a formatter """
  def wrapper(formatterFn):
    registrar.Register(name, formatterFn)
    return formatterFn

  return wrapper
