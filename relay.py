import RPi.GPIO as GPIO
from datetime import datetime
import time

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

	# Set relay high. If user inputs a 1, reset highTime as well
	# Reset highTime if you've used it, particularly if you've just triggered an event with it.
	def setHigh(self, reset = 1):
		GPIO.output(self.pinNum, GPIO.LOW) # Backwards on my relay model (don't know why)
		self.relayState = 1
		if reset == 1:
			self.highTime = "unset"

	# Set relay low. If user inputs a 1, reset lowTime as well
	# Reset lowTime if you've used it, particularly if you've just triggered an event with it.
	def setLow(self, reset = 1):
		GPIO.output(self.pinNum, GPIO.HIGH) # Backwards on my relay model (don't know why)
		self.relayState = 0
		if reset == 1:
			self.lowTime = "unset"

	# Reset highTime
	def resetHighTime(self):
		self.highTime = "unset"

	# Reset lowTime
	def resetLowTime(self):
		self.lowTime = "unset"

	# Check if it's the relay's high time. If it is, return true, set high, and reset highTime.
	def checkHigh(self):
		now = datetime.now()
		nowStr = str(now)[11:19] # Format as string
		if self.highTime == nowStr:
			self.setHigh()
			return(True)
		else:
			return(False)

	# Check if it's the relay's low time. If it is, return true, set low and reset lowTime.
	def checkLow(self):
		now = datetime.now()
		nowStr = str(now)[11:19] # Format as string
		if self.lowTime == nowStr:
			self.setLow()
			return(True)
		else:
			return(False)

	# Set relay high if currently low or low if currently high
	def toggle(self):
		if self.relayState == 1:
			self.setLow()
		else:
			self.setHigh()

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

		# Add to the minute
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