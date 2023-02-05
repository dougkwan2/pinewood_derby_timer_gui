#!/usr/bin/python3

import time
import tkinter as tk
import tkinter.messagebox

import config
import racePanel
#import sensorPanel
import subprocess
import threading
#import timer
import arduinoTimer as timer

numSensors = len(config.sensorPins)
sensorMap = { p : i for i, p in enumerate(config.sensorPins)  }
isEnabled = [ True ] * numSensors
isRunning = [ False ] * numSensors
t = timer.timer()
root = None
panel = None
fpsToMph = 3600.0 / 5280.0
countDown = None
beepThread = None
sensor_panel = None

def calcSpeed(t):
  if t > 0:
    speed = config.trackLength / t * fpsToMph * config.mphScale
    return 999 if speed > 999 else speed
  else:
    return 999

def recordResults():
  resultsFile = open(config.resultsFile, 'a')
  resultsFile.write('race end at ' + time.ctime() + '\n')
  results = []
  for i in range(numSensors):
    track = i + 1
    if isEnabled[i]:
      driver = panel.entry(i).get()
      elapsed = panel.timerView(i).getValue()
      mph = panel.mphView(i).getValue()
      results.append((track, driver, elapsed, mph))

  resultsFile.write('track, driver, elapsed, mph\n')
  for r in sorted(results, key = lambda t : t[2]):
    resultsFile.write('%d, %s, %g, %d\n' % r)
 
  resultsFile.write('\n')
  resultsFile.close()
  
def refreshCallback():
  global isRunning
  if countDown:
    return
  runningStatus = t.getRunningStatus()
  timerValues = t.getTimerValues()
  for i in range(len(runningStatus)):
    if not isEnabled[i]:
      runningStatus[i] = False;
  anyTimerRunning = any(runningStatus)
  for i in range(numSensors):
    if isEnabled[i] and isRunning[i]:
      elapsed = timerValues[i]
      panel.timerView(i).setValue(elapsed)
      if not runningStatus[i]:
        isRunning[i] = False
        panel.mphView(i).setValue(calcSpeed(elapsed))

  if anyTimerRunning:
    root.after(config.refreshms, refreshCallback)
  else:
    recordResults()
    panel.unlockEnables()

def doBeep(beep):
  subprocess.call(["aplay", "-q", beep])

def canStartRace():
  if any(isRunning):
    return False

  tracks_enabled = [panel.enabled(i) for i in range(numSensors)]
  if not any(tracks_enabled):
    tk.messagebox.showerror(message="Need to have at least 1 active track")
    return False

  # check that all active sensors have sufficient light level at start
  low_light_sensor_names = []
  values = t.getSensorValues()
  for i, enabled in enumerate(tracks_enabled):
    if enabled and values[i] < config.sensorThresholds[i]:
      low_light_sensor_names.append(str(i + 1))
  if len(low_light_sensor_names) > 0:
    error_message=("Insufficient light level for sensor(s) " +
                   ",".join(low_light_sensor_names))
    tk.messagebox.showerror(message=error_message)
    return False

  return True

def startCallback():
  global isRunning, isEnabled, countDown
  if not canStartRace():
    return

  panel.reset()
  t.reset()
  panel.lockEnables()
  isEnabled = [panel.enabled(i) for i in range(numSensors)]
  isRunning = isEnabled.copy()
  countDown = None
  v = t.getSensorValues()

  t.start()
  root.after(config.refreshms, refreshCallback)

def countDownCallback():
  global countDown
  global beepThread

  if countDown != None:
    beep = config.shortBeep if countDown > 0 else config.longBeep
    beepThread = threading.Thread(target=doBeep, args=(beep,))
    beepThread.start()
    if countDown > 0:
      countDown = countDown - 1
      root.after(1000, countDownCallback)
    else:
      root.after(0, startCallback)

def delayedStartCallback():
  global countDown

  if not canStartRace():
    return
  panel.reset();
  panel.lockEnables()
  t.reset()
  countDown = 3
  root.after(0, countDownCallback)

def resetCallback():
  global isRunning
  t.reset()
  isRunning = [ False ] * numSensors
  panel.reset();
  panel.unlockEnables()

def doNothing():
  pass

def doTimerInfo():
  info = t.getInfo()
  tk.messagebox.showinfo(title="Timer Information",
                         message="\n".join(info))

def doSensorPanel():
  sensor_panel.deiconify()
  
def doTimerReset():
  t.reset()

def main():
  global root, panel

  t.reset()
  t.setSensorThresholds(config.sensorThresholds)

  root = tk.Tk()

  # Add menu
  menubar = tk.Menu(root)
  menubar.add_command(label="Exit", command=root.quit)

  timer_menu = tk.Menu(menubar, tearoff=0)
  timer_menu.add_command(label="Reset", command = doTimerReset)
  timer_menu.add_command(label="Calibrate", command = doSensorPanel)
  timer_menu.add_command(label="Info", command = doTimerInfo)
  menubar.add_cascade(label="Timers", menu=timer_menu)

  #gates_menu = tk.Menu(menubar, tearoff=0)
  #gates_menu.add_command(label="Up", command=doNothing)
  #gates_menu.add_command(label="Down", command=doNothing)
  #gates_menu.add_command(label="Calibrate", command=doNothing)
  #menubar.add_cascade(label="Gates", menu=gates_menu)
  
  root.config(menu=menubar)

  tk.Label(root, text = "Pinewood Derby", font = config.font).grid(row = 0)
  panel = racePanel.racePanel(root, numSensors)
  panel.grid(row = 1, column = 0)

  frame = tk.Frame(root)
  frame.grid(row=2, column = 0)

  tk.Button(frame, text = "3 secs", command = delayedStartCallback,
            font = config.font).grid(row = 0, column = 0)
  tk.Button(frame, text = "Start", command = startCallback,
            font = config.font).grid(row = 0, column = 1)
  tk.Button(frame, text = "Reset", command = resetCallback,
            font = config.font).grid(row = 0, column = 2)
  resetCallback()

  # Add sensor panel
  # sensor_panel = sensorPanel.sensorPanel(root, numSensors)

  root.mainloop()

if __name__ == "__main__":
  main()
