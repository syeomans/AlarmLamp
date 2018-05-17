import RPi.GPIO as GPIO

# Pin definitions
GPIO.setmode(GPIO.BOARD)
RELAY = 11
PB1 = 13
PB2 = 15
PB3 = 19

# Read alarm times from times.txt
alarmTimes = [line.strip() for line in open("times.txt", 'r')]

# Variables to store when Music state begins and 15 minutes past
musicTriggered = False
musicTime = ""
musicTimePlus = ""

# Variables to store when Alarm state begins and 15 minutes past
alarmTriggered = False
alarmTime = ""
alarmTimePlus = ""