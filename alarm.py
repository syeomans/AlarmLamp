# This script controlls the relay attached to my alarm clock lamp.

# Import modules
import time
import RPi.GPIO as GPIO
from datetime import datetime

# Pin definitions
GPIO.setmode(GPIO.BOARD)
RELAY = 11
PB1 = 13
PB2 = 15

# Pin setup
# GPIO.setup(RELAY, GPIO.OUT) # moved to class initialization
GPIO.setup(PB1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PB2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Class definition for Relay
class Relay:
	# Initialize relay
	def __init__(self, pn):
		self.pinNum = pn
		self.relayState = 0
		self.lowTime = "unset" # time to set relay low
		self.highTime = "unset" # time to set relay high
		GPIO.setup(self.pinNum, GPIO.OUT)
		GPIO.output(self.pinNum, GPIO.LOW)

	# Set relay low. If user inputs a 1, reset lowTime as well
	# Reset lowTime if you've used it, particularly if you've just triggered an event with it.
	def setLow(self, reset = 1):
		GPIO.output(self.pinNum, GPIO.LOW) # Backwards on my relay model (don't know why)
		self.relayState = 0
		if reset == 1:
			self.lowTime = "unset"

	# Set relay high. If user inputs a 1, reset highTime as well
	# Reset highTime if you've used it, particularly if you've just triggered an event with it.
	def setHigh(self, reset = 1):
		GPIO.output(self.pinNum, GPIO.HIGH) # Backwards on my relay model (don't know why)
		self.relayState = 1
		if reset == 1:
			self.highTime = "unset"

	# Reset highTime
	def resetHighTime(self):
		self.highTime = "unset"

	# Reset lowTime
	def resetLowTime(self):
		self.lowTime = "unset"

	# Set relay high if currently low or low if currently high
	def toggle(self):
		if self.relayState == 1:
			self.setLow()
		else:
			self.setHigh()

	# Set relay high for one hour
	def oneHour(self):
		# Set the relay high
		self.setHigh(0)

		# Get current time and clip off everything that isn't hr:mn:sc
		now = datetime.now()
		nowStr = str(now)[11:19]

		# Separate hour, minute, second
		nowSec = nowStr[6:8]
		nowMin = nowStr[3:5]
		nowHr = nowStr[0:2]

		# Add 1 to the hour
		delHr = int(nowHr)+1
		if delHr == 25:
			delHr = "00"
		elif delHr < 10:
			delHr = "0"+str(delHr)

		# Return delayed hr:mn:sc
		delayedTime = str(delHr)+":"+nowMin+":"+nowSec
		self.lowTime = delayedTime

	# Set relay high/low for [delay] minutes. If a time exists, add to the delayed time.
	def setMinutes(self, mode, delay): 
		# If mode is "high," set relay high for [delay] minutes
		if(mode == "high"):
			self.setHigh(0)

			# If input time is unset, get current time and clip off everything that isn't hr:mn:sc
			if(self.lowTime == "unset"):
				self.lowTime = datetime.now()
				timeStr = str(self.lowTime)[11:19]
			else:
				timeStr = self.lowTime

		# Else if mode is "low," set relay low for [delay] minutes
		elif(mode == "low"):
			self.setLow(0)

			# If input time is unset, get current time and clip off everything that isn't hr:mn:sc
			if(self.highTime == "unset"):
				self.highTime = datetime.now()
				timeStr = str(self.highTime)[11:19]
			else:
				timeStr = self.highTime

		# Else, print error
		else:
			print('Invalid mode type. Must be either "high" or "low."')

		# Separate hour, minute, second
		timeSec = timeStr[6:8]
		timeMin = timeStr[3:5]
		timeHr = timeStr[0:2]

		# Add 10 to the minute
		delMin = int(timeMin)+delay
		if delMin >= 60:
			delMin = "0"+str(delMin-60)
			timeHr = str(int(timeHr)+1)
		elif delMin < 10:
			delMin = "0"+str(delMin)

		# if hour is 24 or over, roll over to 0
		if (int(timeHr) >= 24):
			timeHr = "00"
		# if hour is under 10, insert a 0 in front
		elif (int(timeHr) < 10):
			timeHr = "0" + str(int(timeHr))

		# Set high or low timer to delayed hr:mn:sc
		delayedTime = timeHr+":"+str(delMin)+":"+timeSec
		if(mode == "high"):
			self.lowTime = delayedTime
		elif(mode == "low"):
			self.highTime = delayedTime

	# Blink three times and set relay high for one hour
	def alarm(self):
		for i in range(0,3):
			self.setHigh()
			time.sleep(1)
			self.setLow()
			time.sleep(1)
		self.oneHour()
		self.setHigh()

##### End Relay class #####

# Create lamp, an object of Relay class, from pin 11 (RELAY)
lamp = Relay(RELAY)

# Read alarm times from times.txt (reset necessary if edited)
alarmTimes = [line.strip() for line in open("times.txt", 'r')]


# Blink once at the beginning to show the script is working 
lamp.setHigh()
time.sleep(1)
lamp.setLow()
time.sleep(1)

try:
	# Main loop
	running = True
	while running: 

		# Get the current time. This will be compared against other things later. 
		now = datetime.now()
		nowStr = str(now)[11:19] # Format as string
		nowStrW = str(datetime.today().weekday())+" "+str(datetime.now())[11:19] # include weekday

		# Check for a change in the input file
		infile = open("input.txt", "r")
		command = infile.read()
		infile.close()
		# If there's been a change, hold your damn horses and let the change finish.
		# Wait for 0.1 seconds in case the change is still being written and then open the file again.
		if command.strip() != "nothing":
			time.sleep(0.1)
			infile = open("input.txt", "r")
			command = infile.read()
			infile.close()
		# If the command is "stop," end main loop and overwrite input file to reset command ("nothing")
		if command.strip() == "stop":
			running = False
			# Overwrite command after executing
			infile = open("input.txt", "w")
			command = "nothing"
			infile.write(command)
			infile.close()

		# If command is "nothing," do nothing. Else, try to execute the command.
		elif command.strip() != "nothing":
			# Try to execute command. If command can't be executed, continue
			try:
				exec command
				# Overwrite command after executing
				infile = open("input.txt", "w")
				command = "nothing"
				infile.write(command)
				infile.close()
				# For some reason, I have to write twice for it to work
				infile = open("input.txt", "w")
				command = "nothing"
				infile.write(command)
				infile.close()
			except NameError:
				continue

		# Check for lamp's high time.
		# If now is lamp's high time, set high and reset high time.
		if lamp.highTime == nowStr:
			lamp.setHigh(1)

		# Check for lamp's low time.
		# If now is lamp's low time, set low and reset low time.
		if lamp.lowTime == nowStr:
			lamp.setLow(1)

		# Check for alarm times
		if nowStrW in alarmTimes:
			# Sound alarm: blink every 10 seconds for 10 minutes or until a button is pressed
			lamp.alarm()

		# Press pushbutton 1 to toggle the lamp
		if (GPIO.input(PB1) == 1):
			while(GPIO.input(PB1) == 1):
				time.sleep(0.1)
			# If double-pressed pushbutton 1, set high for one minute (or add another minute)
			temp = 0
			doubleClick = 0
			while (temp < 10000):
				temp += 1
				if (GPIO.input(PB1) == 1):
					while(GPIO.input(PB1) == 1):
						time.sleep(0.1)
					doubleClick = 1
					lamp.setMinutes("high", 1)
					break
			if(doubleClick == 0):
				lamp.toggle()

		# Press pushbutton 2
		if (GPIO.input(PB2) == 1):
			while(GPIO.input(PB2) == 1):
				time.sleep(0.1)
			lamp.setMinutes("high", 10)

# If keyboard interrupt
except KeyboardInterrupt:
	GPIO.output(RELAY, GPIO.LOW)
	
# Exit cleanly
finally:
	GPIO.cleanup()
