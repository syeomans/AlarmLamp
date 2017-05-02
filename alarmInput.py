# This script writes input commands to a file used in my alarm clock lamp.
import time
running = True
while running:
	# Get user input
	command = raw_input("Enter a command: \n")
	command = command.lower()
	output = "test"

	# Check user's input to make sure it can be executed. If not, report error.
	
	# If user enters "on," write "lamp.setHigh()"
	if command == "on":
		output = "lamp.setHigh()"
		print("Command written. \n")

	# If user enters "on x," write "lamp.setMinutes("high", x)"
	elif command[0:3] == "on ":
		output = "lamp.setMinutes('high', " + str(command[3:]) +")"
		print("Command written. \n")
	# If user enters "off," write "lamp.setLow()"
	elif command == "off":
		output = "lamp.setLow()"
		print("Command written. \n")
	# If user enters "off x," write "lamp.setMinutes('low', x)"
	elif command[0:4] == "off ":
		output = "lamp.setMinutes('low', " + str(command[4:]) +")"
		print("Command written. \n")
	# If user enters "stop," write "stop" and kill script
	elif command == "stop":
		output = "stop"
		print("Command written. \n")
		running = False
	# Else, the user's command is invalid/unsupported
	else:
		output = "nothing"
		print("Command not recognized.")

	# Write user's command to file input.txt
	outfile = open("input.txt", "w")
	outfile.write(output)
	outfile.close

	# For whatever reason, the file has to be written twice to update correctly
	outfile = open("input.txt", "w")
	outfile.write(output)
	outfile.close
