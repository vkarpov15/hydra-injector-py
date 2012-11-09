#
# cmd_line_sample.py
#
# Created on: November 3, 2012
# Author: Valeri Karpov
#
# An example usage of CommandLineInjector - a very general method for stripping
# padding from a sample file. While this is a somewhat trivial example, it
# highlights some of the more useful features of this library - managing object
# ("square") life cycle, wiring two methods / "circles" together, constructing
# squares from command line params, and a minimum of non-reusable boilerplate
#

from CommandLineInjector import *
import inspect

class FileReader:
  inject = ["infile"]

  def __init__(self, infile):
    self.filename = infile
    print infile

  def initialize(self):
    self.f = open(self.filename, "r")

  def close(self):
    self.f.close()

  def getLines(self):
    return self.f.readlines()

class FileWriter:
  inject = ["outfile"]

  def __init__(self, outfile):
    self.filename = outfile
    print outfile

  def initialize(self):
    self.f = open(self.filename, "w")

  def close(self):
    self.f.close()

  def writeLine(self, line):
    self.f.write("%s\n" % line)

def removePaddingFromFile(reader):
  lines = reader.getLines()
  newLines = [line.strip() for line in lines]
  return newLines

def writeUnpaddedFile(writer, lines = "method:removePaddingFromFile"):
  for line in lines:
    writer.writeLine(line)

#### This is boilerplate
#### Sample run: python cmd_line_sample.py writeUnpaddedFile --f="../test" --outfile=../test2
class MyRunner:
  def run(self, method, params):
    return eval(method)(**params)

  def getSpecs(self, method):
    return inspect.getargspec(eval(method))

# Binding magic. Roughly translated:
#   1) Whenever a method or class asks for something called "reader", it means
#      a FileReader where the constructor parameter "infile" is taken from
#      command line parameter -f
#   2) Similar to above, "writer" is a FileWriter where all of its constructor
#      parameters are taken from command line parameter with same name
# 3/4) Add the methods removePaddingFromFile and writeUnpaddedFile as callable
#      methods from command line
#   5) Run using command line arguments using the runner from this scope
CommandLineInjector().addClass("reader", FileReader, { "infile" : "f" }).addClass("writer", FileWriter).addMethod("removePaddingFromFile").addMethod("writeUnpaddedFile").run(MyRunner())
