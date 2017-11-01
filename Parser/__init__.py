__all__ = ['GetComponentsFromFiles']

from threading import Thread
from random import randint


def GetComponentsFromFiles(files):
  """ Searches a list of files for components """

  thread_list = [] # List of threads

  component_list = [] # List of components

  # Start a new thread for every file in the list
  for file in files[:1]:
    t = Thread(target=fileParseThread, args=(file, component_list))
    t.start()
    thread_list.append(t)

  # Wait until all threads are finished
  for mythread in thread_list:
    mythread.join()


  #for i in component_list:
   # print(i)

  return component_list


def fileParseThread(file, component_list):
  """ Function used as a thread to parse components from files """
  for line in getLine(file):
    print(line)




def getLine(file):
  """ Generator for getting each line of a file one at a time """
  f = open(file)

  for line in iter(f):
    yield line

  f.close()
