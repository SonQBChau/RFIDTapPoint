#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pygame
from time import sleep
import time
import datetime
from neopixel import *
import argparse
from firebase import firebase

# LED strip configuration:
LED_COUNT      = 93      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create Pygame mixer object 
pygame.mixer.init()
#pygame is picky, wav file should be 16 bitdepth
soundSuccess = pygame.mixer.Sound("sounds/happy_34.wav")
soundSuccessEmployee = pygame.mixer.Sound("sounds/ding_1.wav")
soundError = pygame.mixer.Sound("sounds/happy_2.wav")

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

# Intialize RFID reader
reader = SimpleMFRC522()

# Create Firebase object 
firebase = firebase.FirebaseApplication('https://findmykid-51edc.firebaseio.com/', None)


"""
FUNCTIONS CONTROL FOR LIGHT STRIP
"""
DOT_COLORS = [  0x200000,   # red
		0x201000,   # orange
		0x202000,   # yellow
		0x002000,   # green
		0x002020,   # lightblue
		0x000020,   # blue
		0x100010,   # purple
		0x200010 ]  # pink


def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
 
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
                
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(30):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
        
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def colorBreath():
    """Breathing effect animation."""
    for j in range(3):
        #Fade IN
        for k in range(100):
            color = Color(0, 0, 0)
            if j == 0:
                color = Color(k, 0, 0)
            elif j == 1:
                color = Color(0, k, 0)
            elif j == 2:
                color = Color(0, 0, k)
            colorWipe(strip, color)
            time.sleep(5/1000.0)
        # Fade OUT
        for k in range(100, 0, -1):
            color = Color(0, 0, 0)
            if j == 0:
                color = Color(k, 0, 0)
            elif j == 1:
                color = Color(0, k, 0)
            elif j == 2:
                color = Color(0, 0, k)
            colorWipe(strip, color)
	    time.sleep(5/1000.0)
    
def colorBounce():
    """Color bounce from start to end animation."""
    eyeSize = 10
    rangeEye = LED_COUNT - eyeSize - 2
    speedDelay = 20
    returnDelay = 100
    
    for i in range(0, rangeEye, 1):
        colorLess = Color(0, 0, 0)
        colorWipe(strip, colorLess)
        colorHigh= Color(0, 100, 0)
        colorLow = Color (0, 10, 0)
        strip.setPixelColor(i, colorLow)
        for j in range(1, eyeSize, 1):
            strip.setPixelColor(i+j, colorHigh)
        strip.setPixelColor(j+eyeSize+1, colorLow)
        strip.show()
        time.sleep(speedDelay/1000.0)
            
    time.sleep(returnDelay/1000.0)
        
    for i in range(rangeEye,0 ,-1):
        colorLess = Color(0, 0, 0)
        colorWipe(strip, colorLess)
        colorHigh= Color(0, 100, 0)
        colorLow = Color (0, 10, 0)
        strip.setPixelColor(i, colorLow)
        for j in range(1, eyeSize, 1):
            strip.setPixelColor(i+j, colorHigh)
        strip.setPixelColor(j+eyeSize+1, colorLow)
        strip.show()
        time.sleep(speedDelay/1000.0)
        
    time.sleep(returnDelay/1000.0)
    
    colorWipe(strip, Color(0,0,0))
    
"""
FUNCTIONS CONTROLLER FOR PLAY
"""
def playSuccess():
    print ('success sound for kid....')
    soundSuccess.play()
    playLightSuccess()
    #sleep(3)
    soundSuccess.stop()

def playSuccessEmployee():
    print ('success sound for employee...')
    soundSuccessEmployee.play()
    playLightSuccessEmployee()
    sleep(1)
    soundSuccessEmployee.stop()


def playSuccessParent():
    print ('success sound for employee...')
    soundSuccessEmployee.play()
    playLightSuccessParent()
    sleep(1)
    soundSuccessEmployee.stop()
    
def playError():
    print ('error sound....')
    soundError.play()
    playLightError()
    sleep(1)
    soundError.stop()

def playLightSuccess():
    print ('success color....')
    theaterChaseRainbow(strip)
    colorWipe(strip, Color(0,0,0))

def playLightError():
    print ('error color....')
    for i in range(3):
        colorWipe(strip, Color(0, 255, 0))
        time.sleep(0.4)
        colorWipe(strip, Color(0,0,0))
        time.sleep(0.3)

def playLightSuccessEmployee():
    print ('employee color....')
    for i in range(1):
        colorWipe(strip, Color(255,0 , 0))
        time.sleep(0.4)
        colorWipe(strip, Color(0,0,0))
        time.sleep(0.3)

def playLightSuccessParent():
    print ('parent color....')
    for i in range(1):
        colorWipe(strip, Color(0,0 , 255))
        time.sleep(0.4)
        colorWipe(strip, Color(0,0,0))
        time.sleep(0.3)
        
def playLightTest():
    colorBreath()
    colorBounce()

"""
LOOP FOR RFID READER WAITING TO BE SCANNED
"""
try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id, text))
        """
            KID ID: 165068935866
            PARENT ID: 225094668797
            EMPLOYEE ID: 225111446012
        """
        
        # replace with the device ID
        if id == 165068935866: # REPLACE THIS WITH THE ID CARD FOR CHILD
            
            # update entry
            firebaseID = '165068935866' # KID ID
            url = '/KidsClubLog/{}'.format(firebaseID)
            result = firebase.get(url, None)

            # success, update to Firebase 
            if result:
                firebase.put(url, 'Read', 1)
                firebase.put(url, 'Time', datetime.datetime.now())

            else:
                print('This ID does not exist!')

            
            # print debug
            result = firebase.get('/KidsClubLog', None)
            print (result)
            
            # play sound and light
            playSuccess()
          
            #sleep(1)
            
        elif id == 225094668797: # REPLACE THIS WITH THE ID CARD FOR PARENT
            # update entry
            firebaseID = '225094668797' # PARENT ID
            url = '/KidsClubLog/{}'.format(firebaseID)
            result = firebase.get(url, None)

            # success, update to Firebase 
            if result:
                firebase.put(url, 'Read', 1)
                firebase.put(url, 'Time', datetime.datetime.now())
            else:
                print('This ID does not exist!')

            
            # print debug
            result = firebase.get('/KidsClubLog', None)
            print (result)
            
            # play sound and light
            playSuccessParent()
            
        elif id == 225111446012: # REPLACE THIS WITH THE ID CARD FOR EMPLOYEE
            # update entry
            firebaseID = '225111446012' # EMPLOYEE ID
            url = '/KidsClubLog/{}'.format(firebaseID)
            result = firebase.get(url, None)

            # success, update to Firebase 
            if result:
                firebase.put(url, 'Read', 1)
                firebase.put(url, 'Time', datetime.datetime.now())
            else:
                print('This ID does not exist!')

            
            # print debug
            result = firebase.get('/KidsClubLog', None)
            print (result)
            
            # play sound and light
            playSuccessEmployee()
            
        else: # ANY OTHER CARDS WILL MAKE IT INVALID
            playError()
            #print("Playing Light Test...")
            #playLightTest()
            

finally:
        GPIO.cleanup()
        colorWipe(strip, Color(0,0,0), 10)
        
        
        
