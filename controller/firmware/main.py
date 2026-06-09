# main.py
# MicroPython firmware for the Raspberry Pi Pico.
# This is the timing authority for the bot: it drives the optocouplers that press
# the DS4 buttons. It listens for simple text commands over USB serial and acts.
# Keep this file simple. The PC side does the thinking; the Pico presses buttons.

import sys
import time
import uselect
from machine import Pin

# Maps a button name to the Pico GP pin that drives its optocoupler.
# Driving a pin HIGH turns the optocoupler on, which presses the button.
# Driving a pin LOW turns it off, which releases the button.
# Wire each optocoupler to match this map.
BUTTON_PINS = {
    "up": 0,
    "down": 1,
    "left": 2,
    "right": 3,
    "cross": 4,
    "circle": 5,
    "square": 6,
    "triangle": 7,
}

# Holds the Pin object for each button after setup.
pins = {}

# Create one output pin per button and make sure every button starts released.
for name, gpio in BUTTON_PINS.items():
    p = Pin(gpio, Pin.OUT)
    p.value(0)
    pins[name] = p


# Presses a button by turning its optocoupler on.
def press(name):
    pins[name].value(1)


# Releases a button by turning its optocoupler off.
def release(name):
    pins[name].value(0)


# Releases every button. Used as a safety reset.
def release_all():
    for p in pins.values():
        p.value(0)


# Presses a button, waits the given milliseconds, then releases it.
# This is a blocking tap, mainly for simple bring-up tests.
def tap(name, ms):
    press(name)
    time.sleep_ms(ms)
    release(name)


# Handles one full command line and returns the text reply to send back.
def handle(line):
    # Split the line into whitespace separated parts.
    parts = line.split()
    # Ignore empty lines.
    if not parts:
        return ""
    # The first word is the command, upper-cased so case does not matter.
    cmd = parts[0].upper()
    # Replies to a health check so the PC knows the Pico is alive.
    if cmd == "PING":
        return "PONG"
    # Presses and holds a button.
    if cmd == "PRESS" and len(parts) == 2 and parts[1] in pins:
        press(parts[1])
        return "OK"
    # Releases a button, or releases all buttons.
    if cmd == "RELEASE" and len(parts) == 2:
        # RELEASE ALL is a safety reset for every button.
        if parts[1].upper() == "ALL":
            release_all()
            return "OK"
        # Otherwise release the single named button.
        if parts[1] in pins:
            release(parts[1])
            return "OK"
    # Taps a button for a number of milliseconds.
    if cmd == "TAP" and len(parts) == 3 and parts[1] in pins:
        # Convert the millisecond argument to an integer, rejecting bad input.
        try:
            ms = int(parts[2])
        except ValueError:
            return "ERR bad ms"
        tap(parts[1], ms)
        return "OK"
    # Anything we did not understand is reported back as an error.
    return "ERR unknown"


# Set up a poller so we can read serial input without blocking forever.
poller = uselect.poll()
poller.register(sys.stdin, uselect.POLLIN)

# Buffer for characters received until we have a full line.
buffer = ""

# Make sure nothing is pressed when the firmware starts.
release_all()

# Main loop: read characters, build up lines, and handle each finished line.
while True:
    # Wait up to 100 milliseconds for input, then loop again.
    events = poller.poll(100)
    # If no input arrived, go back and wait.
    if not events:
        continue
    # Read a single character from the serial input.
    ch = sys.stdin.read(1)
    # A newline or carriage return ends the current command.
    if ch == "\n" or ch == "\r":
        # Only act if we actually have something buffered.
        if buffer:
            reply = handle(buffer)
            # Send the reply back followed by a newline.
            if reply:
                sys.stdout.write(reply + "\n")
            # Clear the buffer for the next command.
            buffer = ""
    else:
        # Otherwise add the character to the current line buffer.
        buffer += ch
