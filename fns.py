import time
from datetime import datetime
from relay import Relay
import globalvars
import RPi.GPIO as GPIO
import pygame

def blink(relay, n, interval=1):
	for i in range(0,n):
		relay.setHigh()
		time.sleep(interval)
		relay.setLow()
		time.sleep(interval)

def checkPin(pin):
	if (GPIO.input(pin) == 1):
		while(GPIO.input(pin) == 1):
			time.sleep(0.1)
		return(True)
	else:
		return(False)

def checkAlarmTimes():
	nowStrW = str(datetime.today().weekday())+" "+str(datetime.now())[11:19] # include weekday
	if nowStrW in globalvars.alarmTimes:
		return(True)
	else:
		return(False)

def playMusic(file):
	pygame.mixer.init()
	pygame.mixer.music.load(file)
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
	    continue

def addMinutes(timeStr, delay):
	# Separate hour, minute, second
	timeSec = nowStr[6:8]
	timeMin = nowStr[3:5]
	timeHr = nowStr[0:2]

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
	return(delayedTime)