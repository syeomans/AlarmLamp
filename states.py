import fns
from relay import Relay
import globalvars
import os
import time
from datetime import datetime

def state(st, relay):
	outState = st

	"""
	OnOff (default)
		alarmTime --> Music
		button 1 --> OnOff (and Toggle())
		button 2 --> OnOff (and setMinutes("high", 10))
		button 3 --> OnOff (and setMinutes("high", 1)) 
		highTime --> OnOff (and set high)
		lowTime --> OnOff (and set low)
	"""
	if st == "OnOff":

		# Check for alarm times
		if fns.checkAlarmTimes():
			outState = "Music"
			return(outState)

		# Press pushbutton 1 to toggle the lamp
		if fns.checkPin(globalvars.PB1):
			relay.toggle()

		# Press pushbutton 2 to set high for 10 minutes
		if fns.checkPin(globalvars.PB2):
			relay.setMinutes("high", 10)

		# Press pushbutton 3 to set high for 1 minute
		if fns.checkPin(globalvars.PB3):
			relay.setMinutes("high", 1)

		# Check for lamp's high time. If now is lamp's high time, set high and reset high time.
		relay.checkHigh()

		# Check for lamp's low time.
		relay.checkLow()

	
	# Music
	# 	button 1 --> OnOff (and setMinutes("high", 60))
	# 	button 2 --> OnOff (and turn off)
	# 	button 3 --> OnOff (and turn off)
	# 	15 minutes elapse --> Alarm
	
	elif st == "Music":
		now = datetime.now()
		nowStr = str(now)[11:19] # Format as string

		# If just entered this state, play music and trip the trigger
		if globalvars.musicTriggered == False:
			globalvars.musicTriggered = True
			globalvars.musicTime = nowStr
			delayedTime = fns.addMinutes(nowStr, 1)
			globalvars.musicTimePlus = delayedTime
			#fns.playMusic()

		# Press pushbutton 1
		if fns.checkPin(globalvars.PB1):
			relay.setMinutes("high", 60)
			globalvars.musicTriggered = False
			return("OnOff")

		# Press pushbutton 2
		if fns.checkPin(globalvars.PB2):
			relay.setLow()
			globalvars.musicTriggered = False
			return("OnOff")

		# Press pushbutton 3
		if fns.checkPin(globalvars.PB3):
			relay.setLow()
			globalvars.musicTriggered = False
			return("OnOff")

		# If 15 minutes have passed
		if nowStr == globalvars.musicTimePlus:
			globalvars.musicTriggered = False
			return("Alarm")

		# Test for this state
		relay.toggle()
		time.sleep(10)

	# Alarm
	# 	button 1 --> OnOff (set on for 60 minutes)
	# 	button 2 --> OnOff (set off)
	# 	button 3 --> OnOff (set off)
	# 	15 minutes elapse --> OnOff (set off)

	elif st == "Alarm":
		now = datetime.now()
		nowStr = str(now)[11:19] # Format as string

		# If just entered this state, play alarm and trip the trigger
		if globalvars.alarmTriggered == False:
			globalvars.alarmTriggered = True
			globalvars.alarmTime = nowStr
			delayedTime = fns.addMinutes(nowStr, 1)
			globalvars.alarmTimePlus = delayedTime
			#fns.playMusic()

		# Press pushbutton 1
		if fns.checkPin(globalvars.PB1):
			relay.setMinutes("high", 60)
			globalvars.alarmTriggered = False
			return("OnOff")

		# Press pushbutton 2
		if fns.checkPin(globalvars.PB2):
			relay.setLow()
			globalvars.alarmTriggered = False
			return("OnOff")

		# Press pushbutton 3
		if fns.checkPin(globalvars.PB3):
			relay.setLow()
			globalvars.alarmTriggered = False
			return("OnOff")

		# If 15 minutes have passed
		if nowStr == globalvars.alarmTimePlus:
			relay.setLow()
			globalvars.alarmTriggered = False
			return("OnOff")

		# Test for this state
		relay.toggle()
		time.wait(5)

	return(outState)


