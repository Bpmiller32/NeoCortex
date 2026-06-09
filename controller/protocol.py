# protocol.py
# Shared constants for talking to the Pico controller firmware.
# Both the PC client and the firmware must agree on these values.

# The button names the firmware understands.
# These must match the BUTTON_PINS keys in the Pico firmware.
BUTTONS = [
    "up",
    "down",
    "left",
    "right",
    "cross",
    "circle",
    "square",
    "triangle",
]

# The serial baud rate.
# The Pico's USB serial ignores the actual rate, but pyserial still needs a value.
BAUD = 115200

# How long to wait for a reply before giving up, in seconds.
TIMEOUT = 2.0
