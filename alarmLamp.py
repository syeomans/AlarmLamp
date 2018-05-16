# This script controlls the relay attached to my alarm clock lamp.

# Import modules
import time
import RPi.GPIO as GPIO
from datetime import datetime
from relay import Relay
import fns
from globalvars import alarmTimes

# Pin definitions
GPIO.setmode(GPIO.BOARD)
RELAY = 11
PB1 = 13
PB2 = 15
PB3 = 19

# Pin setup
# GPIO.setup(RELAY, GPIO.OUT) # moved to class initialization
GPIO.setup(PB1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PB2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PB3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create lamp, an object of Relay class, from pin 11 (RELAY)
lamp = Relay(RELAY)

# Read alarm times from times.txt (reset necessary if edited)
alarmTimes = [line.strip() for line in open("times.txt", 'r')]

# Blink once at the beginning to show the script is working 
# lamp.setHigh()
# time.sleep(1)
# lamp.setLow()
# time.sleep(1)
fns.blink(lamp, 1)

try:
	# Main loop
	running = True
	while running: 

		# # Get the current time. This will be compared against other things later. 
		# now = datetime.now()
		# nowStr = str(now)[11:19] # Format as string
		# nowStrW = str(datetime.today().weekday())+" "+str(datetime.now())[11:19] # include weekday

		# Check for lamp's high time.
		# If now is lamp's high time, set high and reset high time.
		# if lamp.highTime == nowStr:
		# 	lamp.setHigh(1)
		lamp.checkHigh()

		# Check for lamp's low time.
		# If now is lamp's low time, set low and reset low time.
		# if lamp.lowTime == nowStr:
		# 	lamp.setLow(1)
		lamp.checkLow()

		# Check for alarm times
		# if nowStrW in alarmTimes:
		# 	lamp.alarm()
		if fns.checkAlarmTimes():
			lamp.alarm()

		# Press pushbutton 1 to toggle the lamp
		# if (GPIO.input(PB1) == 1):
		# 	while(GPIO.input(PB1) == 1):
		# 		time.sleep(0.1)
		if fns.checkPin(PB1):
			# If pressed pushbutton 1, set high for one minute
			lamp.setMinutes("high", 60)

		# Press pushbutton 2
		# if (GPIO.input(PB2) == 1):
		# 	while(GPIO.input(PB2) == 1):
		# 		time.sleep(0.1)
		if fns.checkPin(PB2):
			lamp.setMinutes("high", 10)

		# Press pushbutton 3
		# if (GPIO.input(PB3) == 1):
		# 	while(GPIO.input(PB3) == 1):
		# 		time.sleep(0.1)
		if fns.checkPin(PB3):
			lamp.setMinutes("high", 1)

# If keyboard interrupt
except KeyboardInterrupt:
	GPIO.output(RELAY, GPIO.LOW)
	
# Exit cleanly
finally:

	# Blink quickly twice, then exit cleanly
	# lamp.setHigh()
	# time.sleep(0.5)
	# lamp.setLow()
	# time.sleep(0.5)
	# lamp.setHigh()
	# time.sleep(0.5)
	# lamp.setLow()
	# time.sleep(0.5)
	fns.blink(lamp, 2)
	
	GPIO.cleanup()
