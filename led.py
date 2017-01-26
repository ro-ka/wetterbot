import CHIP_IO.GPIO as GPIO
import time
import random
from threading import Thread


PIN = "XIO-P6"
OFF = GPIO.HIGH
ON = GPIO.LOW

GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, OFF)

shouldBlink = False

def start():
  global shouldBlink
  shouldBlink = True

def stop():
  global shouldBlink
  shouldBlink = False
  GPIO.output(PIN, OFF)

def blink():
  while True:
    global shouldBlink
    if shouldBlink == True:
      GPIO.output(PIN, ON)
      time.sleep(random.uniform(0.25, 1.5))
      GPIO.output(PIN, OFF)
      time.sleep(random.uniform(0.1, 0.75))
    else:
      time.sleep(0.2)

blinkThread = Thread(target=blink)
blinkThread.start()