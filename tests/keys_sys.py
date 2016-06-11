#!/usr/bin/python
import time 
import sys
import select

print "Start loop, type 'exit' to exit"

while True:

    print "Reading..."
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline().strip() 

            if (input == "exit"): 
                sys.exit()
            else: 
                print "Wrote '"+input+"'"

    time.sleep(1)