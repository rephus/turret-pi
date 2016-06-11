#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from pygame import mixer
import random
import sys
import select
import math

#Constants
SOUND_FOLDER= "./sounds/"
LANGUAGE = "en"
EXT = ".wav"

#More sounds here http://theportalwiki.com/wiki/Turret_voice_lines#Turret_fire
SOUNDS_DETECTED = ["i_see_you","here_you_are","who_s_there","target_adquired", "firing", "gotcha"]
SOUNDS_MISS = ["are_you_still_there", "target_lost","searching"]
SOUNDS_SEARCH = ["searching", "hello","is_anyone_there", "sentry_mode_activated", "coud_you_come_here"]
SOUNDS_DIE = ["i_dont_blame_you", "i_dont_hate_you", "auauauau", "self_test_error", "resting", "hybernating", "sleep_mode_activated","shutting_down", "no_hard_feelings", "malfunctioning", "critical_error"]
SOUNDS_MOVE = ["stop_shooting", "put_me_down", "wow", "eyeyey", "who_are_you", "please_put_me_down"]

SOUND_FIRE = SOUND_FOLDER+"fire"+EXT
SOUND_PING = SOUND_FOLDER+"ping"+EXT
SOUND_DIE = SOUND_FOLDER+"die"+EXT
SOUND_DEPLOY = SOUND_FOLDER+"deploy"+EXT
SOUND_RETRACT = SOUND_FOLDER+"retract"+EXT

TIME_LOOP = 1 #Time between loops 
TIME_ACTIVE = 5 #Time to wait after activation
TIME_DETECTION = 30 #If last detection is greater than this, the target is missing

NOT_DETECTED = 0
DETECTED = 1

#GPIO PINS
PIN_LED = 12
PIN_PIR = 7
PIN_VIBRATOR = 11

#GPIO setup
GPIO.setmode(GPIO.BOARD)

GPIO.setup(PIN_VIBRATOR, GPIO.OUT)
GPIO.setup(PIN_LED, GPIO.OUT)
GPIO.setup(PIN_PIR, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) 

#Vars
deployed = False
status = NOT_DETECTED
lastDetectionTime = 0

#Functions

def chance(prob):
    return random.randint(0,100) < prob

def isDetected():
    return (time.time() - lastDetectionTime) < TIME_DETECTION

def motion(PIN_PIR):
    global lastDetectionTime
    print "Motion detected! "
    lastDetectionTime = time.time()
    
def randomSound(sounds):
    sound = random.choice(sounds)
    return SOUND_FOLDER + LANGUAGE + "/" + sound + EXT

def speak (sounds) :
    sound = randomSound(sounds)
    mixer.music.load(sound)
    mixer.music.play()
    waitMixerFinish()
    
def waitMixerFinish():
    while mixer.music.get_busy(): 
        time.sleep(1)
    
def shoot():
    
    if (not deployed): 
        deploy()
        
    mixer.music.load(SOUND_FIRE)
    mixer.music.play()
    
    GPIO.output(PIN_VIBRATOR, True)
    waitMixerFinish()
    GPIO.output(PIN_VIBRATOR, False)
    
def ping():
    mixer.music.load(SOUND_PING)
    for i in range(5):
        mixer.music.play()
        time.sleep(1)
    
  
def fadeDown():
    GPIO.output(PIN_LED, True)
    pwm(PIN_LED,100,-1, 2)
    GPIO.output(PIN_LED, False)
    
def fadeUp():
    GPIO.output(PIN_LED, True)
    pwm(PIN_LED,0,1, 2)
    
def pwm (pin, start, increment, totalTime):
    p = GPIO.PWM(PIN_LED, 50)
    p.start(0)
    count = start + increment
    sleep = float(totalTime) / (100 / math.fabs(increment))
    while (count < 100 and count > 0) :
        p.ChangeDutyCycle(count)
        time.sleep(sleep)
        count += increment

def blink():
    
    r = random.uniform(0.01,0.2)
    GPIO.output(PIN_LED, False)
    time.sleep(r)
    GPIO.output(PIN_LED, True)
    time.sleep(r)
    
def die():
    GPIO.output(PIN_LED, True)
    speak(SOUNDS_DIE)
    shoot()
    
    mixer.music.load(SOUND_DIE)
    mixer.music.play()
    for i in range(5):
        blink()
    fadeDown()
    
def pickedUp():
    speak(SOUNDS_MOVE)
    
def deploy():
    mixer.music.load(SOUND_DEPLOY)
    mixer.music.play()
    
def retract():
    mixer.music.load(SOUND_RETRACT)
    mixer.music.play()

def readInput():
    input = ""
    i,o,e = select.select([sys.stdin],[],[],0.0001)
    for s in i:
        if s == sys.stdin:
            input = sys.stdin.readline().strip() 
    if (input == ""):
        pass
    elif (input == "enable"):
        lastDetectionTime = time.time()
    elif (input == "disable"):
        lastDetectionTime = 0
    elif (input == "shoot"):
        shoot()
    elif (input == "pick"):
        pickedUp()
    elif (input == "die"):
        die()
    else:
        print "Unrecognised command "+input
       

#init
mixer.init()

GPIO.add_event_detect(PIN_PIR, GPIO.RISING, callback = motion)

print "Start torret loop, press [CTRL + C] to exit"
#Loop
try:

    while True:

        readInput()

        if (status == NOT_DETECTED and isDetected() ):
            print "Target adquired"
            status = DETECTED
            GPIO.output(PIN_LED, True)
            
            speak(SOUNDS_DETECTED)
            shoot() #Play fire sound and vibration
            ping()
            
        elif (status == DETECTED and isDetected() ):
            #print "Still detected"
            #shoot() #Play fire sound and vibration
            pass
        
        elif (status == DETECTED and not isDetected() ):
            print "Target lost"
            status = NOT_DETECTED
            GPIO.output(PIN_LED, False)
            retract()
            speak(SOUNDS_MISS)
            
        #if (status == NOT_DETECTED and not isDetected() ):
        #    print "Still not detected"
            
        time.sleep(TIME_LOOP)
            
except KeyboardInterrupt:
    print "Quit"
    # Reset GPIO settings
    GPIO.output(PIN_LED, False)
    GPIO.cleanup()

  