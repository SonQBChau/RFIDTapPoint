#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pygame
from time import sleep
import time
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

"""
FUNCTIONS CONTROLLER FOR PLAY
"""
def playSuccess():
    print ('success sound....')
    soundSuccess.play()
    playLightSuccess()
    #sleep(3)
    soundSuccess.stop()

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


"""
LOOP FOR RFID READER WAITING TO BE SCANNED
"""
try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id, text))
        if id == 797256866421: # replace with the device ID card
            
            # update entry
            firebaseID = '225111446012' # replace with ID testing from Firebase: eg. 225111446012
            url = '/KidsClubLog/{}'.format(firebaseID)
            result = firebase.get(url, None)

            # success, update to Firebase 
            if result:
                firebase.put(url, 'Read', 1)
            else:
                print('This ID does not exist!')

            
            # print debug
            result = firebase.get('/KidsClubLog', None)
            print (result)
            
            # play sound and light
            playSuccess()
          
            #sleep(1)
        else:
            playError()
            

finally:
        GPIO.cleanup()
        colorWipe(strip, Color(0,0,0), 10)
        
        
        
