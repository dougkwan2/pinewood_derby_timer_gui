#!/usr/bin/python3

import tkinter as tk
import config
import timerView
import intView

class racePanel:
  def __init__(self, master, tracks=2):
   self.frame = tk.Frame(master)
   colNames = ["Track", "Active", "Driver", "Time", "Scaled mph"]
   for c in range(len(colNames)):
     tk.Label(self.frame, text = colNames[c],
              font=config.font).grid(row=0, column=c)
   self.enableVars = []
   self.enableViews = []
   self.entries = []
   self.enableViews = []
   self.timerViews = []
   self.mphViews = []

   for r in range(1, tracks + 1):
     tk.Label(self.frame, text = str(r),
              font=config.font).grid(row=r, column=0)

     enable_var = tk.IntVar()
     enable_var.set(1)
     cb = tk.Checkbutton(self.frame,
                         variable = enable_var,
                         command=lambda i=r-1: self.enableCallback(i),
                         state=tk.NORMAL)
     self.enableVars.append(enable_var)
     self.enableViews.append(cb)
     cb.grid(row=r, column=1, padx=10)

     v = tk.StringVar()
     en = tk.Entry(self.frame, font=config.font,
                   bg="black", fg="green",
                   insertbackground="green",
                   width=15, textvariable=v)
     self.entries.append(en)
     en.grid(row=r, column=2, padx=10)

     tv = timerView.timerView(self.frame)
     self.timerViews.append(tv)
     tv.grid(row=r, column=3, padx=10)

     mv = intView.intView(self.frame, 3)
     self.mphViews.append(mv)
     mv.grid(row=r, column=4, padx=10)

  def enableCallback(self, i):
    if self.enableVars[i].get() == 1:
      self.entries[i].configure(state=tk.NORMAL)
      self.timerViews[i].configure(state=tk.NORMAL)
      self.mphViews[i].configure(state=tk.NORMAL)
    else:
      self.entries[i].configure(state=tk.DISABLED)
      self.timerViews[i].configure(state=tk.DISABLED)
      self.mphViews[i].configure(state=tk.DISABLED)

  def pack(self, *args):
    self.frame.pack(args)

  def grid(self, **kwargs):
    self.frame.grid(kwargs)
  
  def enabled(self, i):
    return self.enableVars[i].get() == 1

  def timerView(self, i):
    return self.timerViews[i]

  def mphView(self, i):
    return self.mphViews[i]

  def entryView(self, i):
    return self.entries[i]

  def entry(self, i):
    return self.entries[i]

  def reset(self):
    for tv in self.timerViews:
      tv.setValue(0)
    for mv in self.mphViews:
      mv.setValue(0)
 
  def lockEnables(self):
    for ev in self.enableViews:
      ev.configure(state=tk.DISABLED)

  def unlockEnables(self):
    for ev in self.enableViews:
      ev.configure(state=tk.NORMAL)
