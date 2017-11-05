__all__ = ['Pipeline', 'Register', 'Apply']

import os
import Config
import Arguments
import Logger

from .format_registrar import FormatRegistrar


cfg = Config.Get()
args = Arguments.Parse()
registrar = FormatRegistrar()

def Register(name):
  """ Decorator for registering a formatter """
  def wrapper(formatterFn):
    registrar.Register(name, formatterFn)
    return formatterFn

  return wrapper


def Pipeline(nextInPipeline):
	""" Decorator for using the formatter in a pipeline """
	def wrapper(components):
		return nextInPipeline(Apply(components))

	return wrapper


def Apply(components):
  """ Apply the appropriate formatter to the list of components (after middleware) """
  formatter = registrar.Dispatch(args.formatter)

  if formatter is None:
    # Attempt to load formatter from config.json
    formatter = registrar.Dispatch(cfg['formatter'])

    if formatter is None:
      Logger.Fatal("Unkown Formatter", args.formatter)

  # Run through the formatter
  output = formatter(components)

  # Confirm output is a file path
  if not os.path.isfile(str(output)):
    Logger.Fatal("Formatters MUST return the path to the saved file")

  Logger.Log("BOM saved to \"{0}\"".format(output))

  return output


