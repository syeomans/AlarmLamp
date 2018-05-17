# This script controlls the relay attached to my alarm clock lamp.

# Import modules
#import time
import RPi.GPIO as GPIO
#from datetime import datetime
from relay import Relay
import fns
import states

# Pin definitions
GPIO.setmode(GPIO.BOARD)
RELAY = 11
PB1 = 13
PB2 = 15
PB3 = 19

# Pin setup
GPIO.setup(PB1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PB2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PB3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create lamp, an object of Relay class, from pin 11 (RELAY)
lamp = Relay(RELAY)

# Blink once at the beginning to show the script is working 
fns.blink(lamp, 1)

try:
	# Main loop
	running = True
	thisState = "OnOff"
	while running: 

		thisState = states.state(thisState, lamp)

		# # Check for lamp's high time. If now is lamp's high time, set high and reset high time.
		# lamp.checkHigh()

		# # Check for lamp's low time.
		# lamp.checkLow()

		# # Check for alarm times
		# if fns.checkAlarmTimes():
		# 	lamp.alarm()

		# # Press pushbutton 1 to toggle the lamp
		# if fns.checkPin(PB1):
		# 	lamp.toggle()

		# # Press pushbutton 2 to set high for 10 minutes
		# if fns.checkPin(PB2):
		# 	lamp.setMinutes("high", 10)

		# # Press pushbutton 3 to set high for 1 minute
		# if fns.checkPin(PB3):
		# 	lamp.setMinutes("high", 1)

# If keyboard interrupt
except KeyboardInterrupt:
	GPIO.output(RELAY, GPIO.LOW)
	
# Exit cleanly
finally:

	# Blink quickly twice, then exit cleanly
	fns.blink(lamp, 2, 0.5)
	
	GPIO.cleanup()
