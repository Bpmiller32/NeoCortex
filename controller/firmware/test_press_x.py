# test_press_x.py
# A standalone test that runs directly on the Pico from Thonny's Run button.
# It presses the X (cross) button ten times so you can confirm the wiring works.
# This does not need the PC or the serial protocol. Open it in Thonny and Run.

from machine import Pin
import time

# The Pico GP pin wired to the X (cross) button optocoupler.
# Change this number if you wired X to a different GP pin.
X_PIN = 4

# How long each press is held, in seconds.
PRESS_SECONDS = 0.08

# How long to wait between presses, in seconds.
GAP_SECONDS = 0.4

# Set up the X pin as an output and start it released.
x = Pin(X_PIN, Pin.OUT)
x.value(0)

# Press X ten times.
for i in range(10):
    # Press the button.
    x.value(1)
    time.sleep(PRESS_SECONDS)
    # Release the button.
    x.value(0)
    time.sleep(GAP_SECONDS)
    # Show progress in the Thonny shell.
    print("press", i + 1)

# Make sure the button is released at the end.
x.value(0)
print("done")
