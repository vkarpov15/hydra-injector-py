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

class MyRunner:
  def run(self, method, params):
    return eval(method)(**params)

  def getSpecs(self, method):
    return inspect.getargspec(eval(method))

CommandLineInjector().addClass("reader", FileReader).addClass("writer", FileWriter).addMethod("removePaddingFromFile").addMethod("writeUnpaddedFile").run(MyRunner())
