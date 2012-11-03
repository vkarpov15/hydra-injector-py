#
# Injector.py
#
# Created on: April 15, 2012
# Author: Valeri Karpov
#
# Base class for an injector. Handles constructing parameters and executing method calls
#

import inspect
import json

class Injector:

  def __init__(self, params):
    self.nameToClassMap = {}
    self.params = params
    self.instantiated = {}
    self.methods = []
    self.initialize()

  def initialize(self):
    pass

  def addInstantiation(self, key, value):
    self.instantiated[key] = value
    
  def call(self, method, params):
    return eval(method)(**params)

  def getSpecs(self, method):
    return inspect.getargspec(eval(method))

  def handleKeyValidation(self, key, arg = None):
    if arg == None:
      return key
    if arg == "int":
      try:
        key = int(key)
        return key
      except:
        return None
    if arg == "float":
      try:
        key = float(key)
        return key
      except:
        return None
    if arg == "string":
      try:
        return str(key)
      except:
        return None
    if arg == "json":
      try:
        return json.loads(str(key))
      except:
        return None
    if isinstance(arg, tuple):
      if not key in arg:
        return None
      return key
    return key

  def construct(self, runner, key, arg):
    try:
      key = str(key)
    except:
      return None
    if self.instantiated.has_key(key):
      return self.instantiated[key]
    elif self.nameToClassMap.has_key(key):
      typeToInst = self.nameToClassMap[key]
      if len(typeToInst.inject) == 0:
        self.instantiated[key] = typeToInst();
        return self.instantiated[key]
      for dependency in typeToInst.inject:
        params = {}
        good = True
        if self.params.has_key(dependency):
          params[dependency] = self.params[dependency]
        elif self.nameToClassMap[dependency] != None:
          params[dependency] = self.construct(dependency)
          if params[dependency] == None:
            good = False
            break
        else:
          good = False
          break
      if good:
        self.instantiated[key] = typeToInst(**params)
        self.instantiated[key].initialize()
        return self.instantiated[key]
    elif self.params.has_key(key):
      return self.handleKeyValidation(self.cookies[key], arg)
    elif arg != None and isinstance(arg, str) and len(arg) > len("method:") and arg[0:len("method:")] == "method:":
      method = arg[len("method:"):]
      if not method in self.methods:
        return None
      return self.run(method, runner, True)
    elif arg == "optional":
      return ""
    return None
    
  def run(self, method, runner, internal = False):
    if not method in self.methods and (not internal or not method in self.internalMethods):
      return False
 
    inspectData = runner.getSpecs(method)
    argNames = inspectData[0]
    tailDefaults = inspectData[3]
    if tailDefaults == None:
      tailDefaults = []
    
    params = {}
    ctr = 0
    defaultsStart = len(argNames) - len(tailDefaults)
    for arg in argNames:
      if ctr >= defaultsStart:
        default = tailDefaults[ctr - defaultsStart]
      else:
        default = None
      params[arg] = self.construct(runner, arg, default)
      if params[arg] == None:
        if internal:
          return None
        else:
          return False
      ctr += 1
    ret = runner.run(method, params) #self.call(method, params)

    if not internal:    
      for key in self.instantiated:
        self.instantiated[key].close()
    return ret

