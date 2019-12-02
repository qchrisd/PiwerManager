#
# This program watches the status of the PowerBoost 1000C providing power to the Raspberry Pi.
#
# The main loop watches for a falling edge on the USB pin indicating the device has been unplugged.
# The designated person is notified via email when the falling edge is detected. An email will be
# sent to the designated when a rising edge is detected indicating it has been plugged back in.
#
# Secondarily this program will watch the low_bat pin on the PowerBoost and gracefully shut down
# if a low charge is detected.
#


# Import the necessary modules
import RPi.GPIO as gpio
from time import sleep
# Import local modules
import config
import log
from shutdown import shutdown

# Callback functions for when edge is detected
def edgeDetected(channel):

	# Pause for 1 second to let the pin finish falling before polling for status
	sleep(1)

	# Shutdown the Raspberry Pi if the battery is low
	if channel == config.pinLBO and not gpio.input(channel):
		log.logMessage("Low battery detected. Shutting down.")
		shutdown()
	# Logs if the wall power has been unplugged or plugged in
	elif channel == config.pin5V:
		# Rising edge (0 to 1)
		if gpio.input(channel):
			log.logMessage("Wall power plugged in.")
		# Falling edge (1 to 0)
		else:
			log.logMessage("Wall power unplugged.")

# Set up the GPIO pins
gpio.setmode(gpio.BCM)  # Using Broadcom numbering
gpio.setup(config.pin5V, gpio.IN, pull_up_down = gpio.PUD_DOWN)  # Set up an input for wall power
gpio.setup(config.pinLBO, gpio.IN, pull_up_down = gpio.PUD_UP)  # Set up an imput for low battery

# Add the edge detection on this channel. Bouncetime is set to 3s to prevent duplicate activations
gpio.add_event_detect(config.pin5V, gpio.BOTH, callback = edgeDetected, bouncetime = 3000)
gpio.add_event_detect(config.pinLBO, gpio.FALLING, callback = edgeDetected, bouncetime = 3000)

# Main loop utilizing a daemon to run it from the background
try:
	# Pause for 120 seconds to reduce power usage
	while(True):
		sleep(120)
# Stops the loop with keyboard interrupt
except KeyboardInterrupt:
	pass
finally:
	gpio.cleanup()  # Closes the inputs for the GPIO
