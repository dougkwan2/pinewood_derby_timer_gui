#!/usr/bin/env python

font = ("Courier", 32)
sensorPins = [17, 18, 27, 22]
sensorThresholds = [512,512,512,512]
refreshms = 93
trackLength = 32

shortBeep = "sin_800Hz_0.25s.wav"
longBeep = "sin_1600Hz_1s.wav"
# pinewoord length: 7 in
# Honda Civic length: 177.3 in
mphScale = 177.3 / 7

resultsFile = "results.txt"
