#!/usr/bin/python

import config
import Tkinter as tk

class SensorValue:
  def __init__(self, master, variable=None):
    if variable is None:
      variable = tk.IntVar()
    self.variable = variable
    self.textVar = tk.StringVar()
    self.label = tk.Label(master, {"textvariable" : self.textVar,
                                  "font" : config.font,
                                  "borderwidth" : 1,
                                  "bg" : "black",
                                  "fg" : "green"})
    self.textVar.set(SensorValue.numToStr(self.variable.get()))
    variable.trace("w", self.updateStringValue)

  def pack(self, *args):
    self.label.pack(args)

  def grid(self, **kwargs):
    self.label.grid(kwargs)

  def getValue(self):
    return self.variable.get()

  def setValue(self, value):
    self.variable.set(value)

  def updateStringValue(self, var, index, mode):
    self.textVar.set(SensorValue.numToStr(self.variable.get()))

  @staticmethod
  def numToStr(n):
    return "{:6}".format(n)

class Sensor(tk.Frame):
  def __init__(self, parent, timer=None):
    tk.Frame.__init__(self, parent)
    self.parent = parent
    self.timer = timer
    self.widgets()
    self.updateCurrent()

  def widgets(self):
    self.high_button = tk.Button(self, text="High", command=self.readHigh).grid(row=0, column=0)
    self.low_button = tk.Button(self, text="Low", command=self.readLow).grid(row=1, column=0)
    self.threshold_label = tk.Label(self, text="Threshold").grid(row=2, column=0)
    self.current_label = tk.Label(self, text="Current").grid(row=3, column=0)
    self.high=[]
    self.high_widget=[]
    self.low=[]
    self.low_widget=[]
    self.threshold=[]
    self.threshold_widget=[]
    self.current=[]
    self.current_widget=[]
    for i in range(4):
      high_variable = tk.IntVar(name="high_%d" % i)
      self.high.append(high_variable)
      self.high_widget.append(SensorValue(self, high_variable))
      low_variable = tk.IntVar(name="low_%d" % i)
      self.low.append(low_variable)
      self.low_widget.append(SensorValue(self, low_variable))
      threshold_variable = tk.IntVar(name="threshold_%d" % i)
      self.threshold.append(threshold_variable)
      self.threshold_widget.append(SensorValue(self, threshold_variable))
      current_variable = tk.IntVar(name="current_%d" % i)
      self.current.append(current_variable)
      self.current_widget.append(SensorValue(self, current_variable))
      high_variable.trace("w", self.updateHighLow)
      low_variable.trace("w", self.updateHighLow)
      col = i+1 
      self.high_widget[i].grid(row=0, column=col, padx=2,pady=2)
      self.low_widget[i].grid(row=1, column=col, padx=2, pady=2)
      self.threshold_widget[i].grid(row=2, column=col, padx=2, pady=2)
      self.current_widget[i].grid(row=3, column=col, padx=2, pady=2)

    self.threshold_percentage = tk.IntVar()
    self.threshold_percentage.trace("w", self.updateAllThresholds)
    self.scale_label = tk.Label(self, text="Threshold percentage").grid(row=0, column=5)
    self.scale = tk.Scale(self, from_=100, to=0, resolution=1,
                          variable=self.threshold_percentage,
                          ).grid(row=1, column=5, rowspan=3, sticky="NS")

  def updateCurrent(self):
    values=self.timer.getSensorValues()
    for i in range(4):
      self.current[i].set(values[i]) 
    self.parent.after(20, self.updateCurrent)

  def readHigh(self):
    values = self.timer.getSensorValues()
    for i in range(4):
      self.high[i].set(values[i])

  def readLow(self):
    values = self.timer.getSensorValues()
    for i in range(4):
      self.low[i].set(values[i])
 
  def updateHighLow(self, var, index, mode):
    var_index = var.split("_")
    if len(var_index) == 2 and var_index[1].isdigit():
      index = int(var_index[1])
      if index >= 0 and index < len(self.threshold):
        self.updateThreshold(index)

  def updateThreshold(self, index):
    high = self.high[index].get()
    low = self.low[index].get()
    percentage = self.threshold_percentage.get()
    threshold = (high * percentage + low * (100 - percentage)) * 0.01
    self.threshold[index].set(threshold)

  def updateAllThresholds(self, var, index, mode):
    for i in range(4):
      self.updateThreshold(i)

  def setHigh(self, index, value):
    self.high[index].set(value)

  def setLow(self, index, value):
    self.low[index].set(value)

  def setThresholdPercentage(self, value):
    self.threshold_percentage.set(value)
