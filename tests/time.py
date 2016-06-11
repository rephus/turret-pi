#!/usr/bin/python
import time 

startTime = time.time()
lastTime = startTime #Time in seconds

print "Time start ",startTime

print "Sleep 1.5 sec"
time.sleep(1.5) 

print "Time after 1.5 sec ",time.time()

difTime = time.time() - lastTime
print "Time since start ",difTime

if (difTime < 2):
    print "difTime < 2"
elif (difTime > 2):
    print "difTime > 2"
    
