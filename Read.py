# ROYAL CARIBBEAN FILE

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import pygame
from time import sleep
import time
import datetime
from neopixel import *
import os
import pyrebase
from threading import Thread
import threading
import sys

# LED strip configuration:
LED_COUNT      = 93      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

dirName = os.path.dirname(__file__)
soundErrorPath = os.path.join(dirName, "sounds/Error_04_Sound.wav")
soundSuccessPath = os.path.join(dirName, "sounds/Success_Alert_5_Sound.wav")

# Create Pygame mixer object 
pygame.mixer.init()
#pygame is picky, wav file should be 16 bitdepth
soundSuccess = pygame.mixer.Sound(soundSuccessPath)
soundError = pygame.mixer.Sound(soundErrorPath)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

# Intialize RFID reader
reader = SimpleMFRC522()

# Create Firebase object 
config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://findmykid-51edc.firebaseio.com",
  "storageBucket": "projectId.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

"""IDLE BACKGROUND THREAD FOR WAITING LIGHT"""
class IdleLightThread(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    can_loop = True
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
    
        thread = Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
    
    def run(self):
        eyeSize = 1
        rangeEye = LED_COUNT - eyeSize
        speedDelay = 30
        returnDelay = 100
        colorLess = Color(0, 0, 0)
        colorHigh= Color(0, 100, 0)
        colorLow = Color (0, 10, 50)
        i = 0
        """ Method that runs forever """
        while i < rangeEye:
            if self.can_loop:
                i = 0 if (rangeEye-1) == i else (i+1)
                colorWipe(strip, colorLess)
                for j in range(0, eyeSize, 1):
                    value = 5 + j* 25
                    dotPosition = (i + j) % LED_COUNT                 
                    strip.setPixelColor(dotPosition, Color(value,value,value))
                strip.show()
                if eyeSize < 10:
                    eyeSize += 1
                time.sleep(speedDelay/1000.0)
            else:
                i = 0
                eyeSize = 1
                
"""COLOR CONTROLLER FUNCTIONS"""                
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def redFadeOut():
    # show light on
    color = Color(0, 200, 0)
    colorWipe(strip, color)
    time.sleep(1000/1000.0)
    # Fade OUT
    for k in range(20, 0, -1):
        color = Color(0, k*10, 0)
        colorWipe(strip, color)
        time.sleep(5/1000.0)
    colorWipe(strip, Color(0,0,0))

def greenFadeOut():
    # show light on
    color = Color(200, 0, 0)
    colorWipe(strip, color)
    time.sleep(1000/1000.0)
    # Fade OUT
    for k in range(20, 0, -1):
        color = Color(k*10, 0, 0)
        colorWipe(strip, color)
        time.sleep(5/1000.0)
    colorWipe(strip, Color(0,0,0))
    
"""
FUNCTIONS CONTROLLER FOR PLAY
"""
def playSuccess():
    print ('success sound...')
    soundSuccess.play()
    playLightSuccess()
    
def playError():
    print ('error sound....')
    soundError.play()
    playLightError()

def playLightSuccess():
    print ('success color....')
    idleLight.can_loop = False
    greenFadeOut()
    idleLight.can_loop = True

def playLightError():
    print ('error color....')
    idleLight.can_loop = False
    redFadeOut()
    idleLight.can_loop = True

"""DATABASE FUNCTION"""    
def updateFirebase(firebaseID):
    db.child("KidsClubLog").child(firebaseID).update({"Read":1, "Time": str(datetime.datetime.now())})
                

"""
INIT WAITING LIGHT THREAD
"""
idleLight = IdleLightThread()

"""LOOP FOR RFID READER"""
try:
    while True:
        sleep(0.5)
        print("Hold a tag near the reader")
        id = reader.read_id()
        print("ID card is: %s" % (id))
        """
            KID CHECKIN ID: 165068935866
            KID CHECKOUT ID: 853040429192
            PARENT ID: 225094668797
            EMPLOYEE ID: 225111446012
            IOS PARENT ID: 1011973426216
            WILDBAND KID CHECKIN ID: 584184446378
        """
        
        # replace with the device ID
        if id == 165068935866: # REPLACE THIS WITH THE ID CARD FOR CHILD CHECKIN     
            firebaseID = '165068935866' # KID CHECKIN ID
            Thread(target=playSuccess).start()
            Thread(target=updateFirebase(firebaseID)).start()


        elif id == 853040429192: # REPLACE THIS WITH THE ID CARD FOR CHILD CHECKOUT   
            firebaseID = '853040429192' # KID CHECKOUT ID
            Thread(target=playSuccess).start()
            Thread(target=updateFirebase(firebaseID)).start()
        
        elif id == 584184446378: # WILDBAND ID 
            firebaseID = '584184446378' # KID CHECKIN ID
            Thread(target=playSuccess).start()
            Thread(target=updateFirebase(firebaseID)).start()
                                
        elif id == 225094668797: # REPLACE THIS WITH THE ID CARD FOR PARENT
            firebaseID = '225094668797' # PARENT ID
            Thread(target=playSuccess).start()
            Thread(target=updateFirebase(firebaseID)).start()
            
        elif id == 1011973426216: # PARENT IOS
            firebaseID = '1011973426216' # PARENT ID
            Thread(target=playSuccess).start()
            Thread(target=updateFirebase(firebaseID)).start()
            
        elif id == 225111446012: # REPLACE THIS WITH THE ID CARD FOR EMPLOYEE
            firebaseID = '225111446012' # EMPLOYEE ID
            Thread(target=playSuccess).start()
            Thread(target=updateFirebase(firebaseID)).start()

        else: # ANY OTHER CARDS WILL MAKE IT INVALID
            playError() 

finally:
        GPIO.cleanup()
        colorWipe(strip, Color(0,0,0), 10)
