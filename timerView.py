#!/usr/bin/python3

import config
import tkinter as tk

class timerView:
  def __init__(self, master):
    self.value = 0
    self.textVar = tk.StringVar()
    self.textVar.set(timerView.secondsToStr(self.value))
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
    self.value = value
    self.textVar.set(timerView.secondsToStr(self.value))

  def configure(self, *args, **kwargs):
    self.label.configure(*args, **kwargs)

  @staticmethod
  def secondsToStr(s):
    whole = int(s)
    decimals = int((s - whole) * 1000)
    whole = whole % 3600
    min = whole // 60
    sec = whole % 60
    return '%02d:%02d.%03d' % (min, sec, decimals)
