"""
Afterware runs after the formatter and operates on the saved file
"""
__all__ = ['Pipeline', 'Register', 'Apply']

import Logger

import tempfile
import os
from shutil import copyfile

from .afterware_registrar import AfterwareRegistrar

import Config

registrar = AfterwareRegistrar()
cfg = Config.Get()


def Register(name):
  """ Decorator for creating Afterware """
  def wrapper(afterwareFn):
    registrar.Register(name, afterwareFn)
    return afterwareFn

  return wrapper


def Pipeline(nextInPipeline):
  """ Decorator for using afteware in a pipeline """
  def wrapper(savedFile):
    return nextInPipeline(Apply(savedFile))

  return wrapper


def Apply(savedFile):
  """ Run the file through afterware """
  # Create a temporary file for the afterware to use,
  # this way the actual BOM will not be deleted or modified
  fileForAfterware = createCopyOfFile(savedFile)

  for afterware in cfg['afterware']:
    afterwareFn = registrar.Dispatch(afterware)

    if afterwareFn is None:
      Logger.Error("Unkown Afterware", afterware)
      continue

    # Run the temp file through afterware
    afterwareFn(fileForAfterware)

  # Cleanup
  if fileForAfterware != savedFile:
    os.remove(fileForAfterware)

  return savedFile


def createCopyOfFile(file):
  """ Creates a copy of the file into a temporary folder """
  filename, ext = os.path.splitext(file)
  tmpFile = os.path.join(tempfile.gettempdir(), "bom.temp{0}".format(ext))

  try:
    copyfile(file, tmpFile)

    # Copy was made
    return tmpFile
  except Exception as e:
    Logger.Error("Could not create a copy of the file", file, " running afterware on that path")
    return file
