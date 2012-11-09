#
# CommandLineInjector.py
#
# Created on: November 3, 2012
# Author: Valeri Karpov
#
# Specialize injector to pull parameters from command line arguments.
#

import sys
from Injector import Injector

class CommandLineInjector:
  def __init__(self):
    if len(sys.argv) < 2:
      print "No method call, can't run"
      sys.exit(0)

    self.op = sys.argv[1]
    params = {}
    for i in range(2, len(sys.argv)):
      if sys.argv[i][0:len("--")] == "--":
        params[sys.argv[i][len("--"):sys.argv[i].find("=")]] = sys.argv[i][sys.argv[i].find("=") + 1:]
      elif sys.argv[i][0] == '-':
        params[sys.argv[i][len("-"):sys.argv[i].find("=")]] = sys.argv[i][sys.argv[i].find("=") + 1:]

    self.injector = Injector(params)

  def initialize(self):
    pass

  def run(self, runner):
    self.injector.run(self.op, runner)

  def addInstantiation(self, key, value):
    self.injector.addInstantiation(key, value)
    return self

  def addMethod(self, method):
    self.injector.methods.append(method)
    return self

  def addClass(self, key, clazz, paramMapping = {}):
    self.injector.addToClassMap(key, clazz, paramMapping)
    return self
