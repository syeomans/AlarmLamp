# This script controlls the relay attached to my alarm clock lamp.

# Import modules
#import time
import RPi.GPIO as GPIO
#from datetime import datetime
from relay import Relay
import fns
import states
from globalvars import *

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
		thisState = states.getNextState(thisState, lamp)

# If keyboard interrupt
except KeyboardInterrupt:
	GPIO.output(RELAY, GPIO.LOW)
	
# Exit cleanly
finally:

	# Blink quickly twice, then exit cleanly
	fns.blink(lamp, 2, 0.5)
	
	GPIO.cleanup()
