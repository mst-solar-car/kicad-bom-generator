from __future__ import absolute_import

import pytest
import os

import Config
from Arguments.argument_parser import ArgumentParser

cfg = Config.Get()

def test_setting_default_arguments():
  """ Tests Parsing Arguments with an invalid number of arguments """
  # Arrange
  expected_project_folder = os.path.split(os.path.abspath(os.getcwd()))[0] + "/"
  expected_formatter = cfg['defaultFormatter']

  # Act
  testArgs = ArgumentParser([])

  # Assert
  assert testArgs.project_folder == expected_project_folder
  assert testArgs.formatter == expected_formatter
  assert testArgs.verbose == False
  assert testArgs.debug == False

  # Cleanup
  ArgumentParser.Reset()


def test_appending_trailing_foward_slash():
  """ Tests to confirm that the Argument Parser will add a trailing forward slash to the project_folder """
  # Arrange
  expected_project_folder = "C:\\NotReal\TestAgain/"
  args = ["C:\\NotReal\TestAgain\File.xml", "C:\\NotReal\TestAgain\Project"]

  # Act
  testArgs = ArgumentParser(args)

  # Assert
  assert testArgs.project_folder == expected_project_folder

  # Cleanup
  ArgumentParser.Reset()

def test_formatter_arg():
  """ Tests to confirm that the Argument Parser sets a formatter """
  # Arrange
  expected_project_folder = "C:\\NotReal\TestAgain/"
  excepted_formatter = "csv"
  args = ["C:\\NotReal\TestAgain\File.xml", "C:\\NotReal\TestAgain\Project", "csv"]

  # Act
  testArgs = ArgumentParser(args)

  # Assert
  assert testArgs.project_folder == expected_project_folder
  assert testArgs.formatter == excepted_formatter

  # Cleanup
  ArgumentParser.Reset()

