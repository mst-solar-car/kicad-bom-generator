from __future__ import absolute_import
import pytest

from Singleton import Singleton

@Singleton
class TestSingleton:
  def __init__(self):
    pass

@Singleton
class AnotherTestSingleton:
  def __init__(self):
    pass



def test_singletons_are_the_same():
  """ Tests that two instances of the same singleton class are the same """
  singleton1 = TestSingleton()
  singleton2 = TestSingleton()

  assert singleton1 is singleton2


def test_singlets_are_different():
  """ Tests that two instances of different singleton classes are not the same """
  singleton1 = TestSingleton()
  singleton2 = AnotherTestSingleton()

  assert singleton1 is not singleton2