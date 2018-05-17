# Read alarm times from times.txt
alarmTimes = [line.strip() for line in open("times.txt", 'r')]

# Variables to store when Music state begins and 15 minutes past
musicTriggered = False
musicTime = ""
musicTimePlus = ""

# Variables to store when Alarm state begins and 15 minutes past
AlarmTriggered = False
AlarmTime = ""
AlarmTimePlus = ""