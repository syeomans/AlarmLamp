import time
from datetime import datetime
from relay import Relay
import globalvars
import RPi.GPIO as GPIO

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