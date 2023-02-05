#!/usr/bin/python3

import config
import serial
import sys

_PORT="/dev/ttyACM0"
_BAUDRATE=76800
_VERBOSE=False

class timer:
  def __init__(self):
    self.serial = serial.Serial(port=_PORT, baudrate=_BAUDRATE, timeout=1)
    reply=''
    while reply != "Hello":
      reply=self.sendCommand("h\n")
    self.sendCommand("f1111")

  def sendCommand(self, cmd):
      self.serial.write(cmd.encode("ascii"))
      reply = self.serial.readline().decode("ascii").strip() 
      if _VERBOSE:
        print("command=", cmd)
        print("reply=", reply)
      return reply
  
  def getTimerValues(self):
    reply = self.sendCommand("v")
    return [int(x) * 0.001 for x in reply[1:].split(',')]

  def getRunningStatus(self):
    reply = self.sendCommand("q")
    return [c == 'G' for c in reply[1:]]

  def start(self):
    reply = self.sendCommand("g")

  def stop(self):
    reply = self.sendCommand("s")

  def reset(self):
    reply = self.sendCommand("c")

  def getInfo(self):
    reply = self.sendCommand("i")
    return reply[1:].split(',')

  def getSensorValues(self):
    reply = self.sendCommand("a")
    return [int(x) for x in reply[1:].split(',')]

  def getSensorThresholds(self):
    reply = self.sendCommand("t")
    return [int(x) for x in reply[1:].split(',')]

  def setSensorThresholds(self, thresholds):
    command="u"+(",".join(map(str, thresholds)))
    reply = self.sendCommand(command)
