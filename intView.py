#!/usr/bin/python3

import tkinter as tk
import config

class intView:
  def __init__(self, master, width):
    self.width = width
    self.format = '%%%dd' % width
    self.blank = ' ' * width
    self.textVar = tk.StringVar()
    self.setValue(0)
    self.label = tk.Label(master, {"textvariable" : self.textVar,
                                   "font" : config.font,
                                   "borderwidth" : 1,
                                   "bg" : "black",
                                   "fg" : "green"})

  def pack(self, *args):
    self.label.pack(args)

  def grid(self, **kwargs):
    self.label.grid(kwargs)

  def getValue(self):
    return self.value

  def setValue(self, value):
    self.value = int(value)
    self.textVar.set(self.valueToStr(self.value))

  def configure(self, *args, **kwargs):
    self.label.configure(*args, **kwargs)

  def valueToStr(self, v):
    if v > 0:
      return self.format % v
    else:
      return self.blank
