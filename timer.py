#!/usr/bin/python

import subprocess
import sys

class timer:
  def __init__(self, executable):
    self.handle = subprocess.Popen(executable, bufsize = 0,
                                   stdin = subprocess.PIPE,
                                   stdout = subprocess.PIPE,
                                   stderr = sys.stderr)   

  def read(self, i):
    self.handle.stdin.write('g %d\n' % i);
    self.handle.stdin.flush();
    reply = self.handle.stdout.readline()
    return float(reply)


  def isRunning(self, i):
    self.handle.stdin.write('l\n');
    self.handle.stdin.flush();
    reply = self.handle.stdout.readline()
    return reply[i] == '1'

  def start(self):
    self.handle.stdin.write('r\n');
    self.handle.stdin.flush();

  def stop(self):
    self.handle.stdin.write('s\n');
    self.handle.stdin.flush();

  def reset(self):
    self.handle.stdin.write('c\n');
    self.handle.stdin.flush();
