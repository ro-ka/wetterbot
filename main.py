import CHIP_IO.GPIO as GPIO
import time
import weather
import led

BUTTON_PIN = "XIO-P7"
GPIO.setup(BUTTON_PIN, GPIO.IN)
old_button_state = None

weather.loadForecast()

dead = False
while not dead:
  try:
    button_state = GPIO.input(BUTTON_PIN)

    if button_state != old_button_state:
      print("Button Pressed")
      old_button_state = button_state
      led.start()
      weather.sayIt()
      led.stop()
      time.sleep(0.5)

  except KeyboardInterrupt:
    dead = True

GPIO.cleanup()
