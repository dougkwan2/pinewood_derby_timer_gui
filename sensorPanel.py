#!/usr/bin/python3

import Tkinter as tk
import config
import intView

class sensorPanel:
  def __init__(self, master, tracks):
   self.frame = tk.Frame(master)
   colNames = ["Enable", "Value", "Threshold"]
   for c in range(len(colNames)):
     tk.Label(self.frame, text = colNames[c],
                   font=config.font).grid(row=0, column=c)
   self.enableViews = []
   self.valueViews = []
   self.thresholdViews = []
   for r in range(1, tracks + 1):
     tk.Label(self.frame, text = str(r),
              font=config.font).grid(row=r, column=0)

     check_var = tk.IntVar()
     en = tk.Checkbutton(self.frame, variable=check_var, onvalue=1,
                              offvalue=0)
     self.enableViews.append(en)
     en.grid(row=r, column=1, padx=10)

     value = intView.intView(self.frame, 5)
     self.valueViews.append(value)
     value.grid(row=r, column=3, padx=10)

     threshold = intView.intView(self.frame, 5)
     self.thresholdViews.append(threshold)
     value.grid(row=r, column=3, padx=10)

  def pack(self, *args):
    self.frame.pack(args)

  def grid(self, **kwargs):
    self.frame.grid(kwargs)
  
  def enableView(self, i):
    return self.enableViews[i]

  def valueView(self, i):
    return self.valueViews[i]

  def threadholdView(self, i):
    return self.threadholdViews[i]

  def entry(self, i):
    return self.entries[i]

  def reset(self):
    for en in self.enableViews:
      en.setEanble(0)
    for value in self.valueViews:
      value.setValue(0)
    for threshold in self.thresholdViews:
      threshold.setValue(0)
