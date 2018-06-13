import fns
from relay import Relay
import globalvars
import os
import time
from datetime import datetime
from pygame import mixer
import os, random

def getNextState(st, relay):
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

		# If a song is not playing, stop mixer
		try:
			if mixer.music.get_busy() == 0:
				mixer.quit()
		except error:
			pass


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
	# 	button 1 --> OnOff (play through song and setMinutes("high", 60))
	# 	button 2 --> OnOff (play through song and turn off)
	# 	button 3 --> OnOff (stop music and turn off)
	# 	15 minutes elapse --> Alarm
	
	elif st == "Music":
		now = datetime.now()
		nowStr = str(now)[11:19] # Format as string

		# If just entered this state, play music and trip the trigger
		if globalvars.musicTriggered == False:
			globalvars.musicTriggered = True
			globalvars.musicTime = nowStr
			delayedTime = fns.addMinutes(nowStr, 15)
			globalvars.musicTimePlus = delayedTime
			mixer.init()

		# If a song is not playing, select one randomly
		if mixer.music.get_busy() == 0:
			song = random.choice(os.listdir(globalvars.folder))
			mixer.music.load(globalvars.folder + '/' + song)
			mixer.music.play()

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
			mixer.music.stop()
			return("OnOff")

		# If 15 minutes have passed
		if nowStr == globalvars.musicTimePlus:
			globalvars.musicTriggered = False
			mixer.music.stop()
			return("Alarm")

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
			delayedTime = fns.addMinutes(nowStr, 5)
			globalvars.alarmTimePlus = delayedTime
			mixer.init()

		# If alarm is not playing, play it again
		if mixer.music.getbusy() == 0:
			song = random.choice(os.listdir(globalvars.folder))
			mixer.music.load(globalvars.folder + '/AnnoyingAlarm/' + song)
			mixer.music.play()

		# Press pushbutton 1
		if fns.checkPin(globalvars.PB1):
			mixer.music.stop()
			relay.setMinutes("high", 60)
			globalvars.alarmTriggered = False
			return("OnOff")

		# Press pushbutton 2
		if fns.checkPin(globalvars.PB2):
			mixer.music.stop()
			relay.setLow()
			globalvars.alarmTriggered = False
			return("OnOff")

		# Press pushbutton 3
		if fns.checkPin(globalvars.PB3):
			mixer.music.stop()
			relay.setLow()
			globalvars.alarmTriggered = False
			return("OnOff")

		# If 5 minutes have passed
		if nowStr == globalvars.alarmTimePlus:
			mixer.music.stop()
			relay.setLow()
			globalvars.alarmTriggered = False
			return("OnOff")

	return(outState)


