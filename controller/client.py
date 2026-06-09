# client.py
# PC-side client for the Pico controller firmware.
# It sends simple text commands over USB serial and reads the replies.
# Higher level code (the timeline and runner modules) will build on this.

import serial
from controller import protocol


# Talks to the Pico over a serial port.
class Controller:
    # Opens the serial connection to the Pico on the given port.
    # On macOS the port looks like /dev/tty.usbmodemXXXX.
    def __init__(self, port):
        # Remember the port name for error messages.
        self.port = port
        # Open the serial connection using the shared settings.
        self.serial = serial.Serial(port, protocol.BAUD, timeout=protocol.TIMEOUT)
        # The assumed length of one game frame in milliseconds.
        # 30 frames per second is about 33.37 ms per frame.
        # We will calibrate this value against the real game later.
        self.frame_ms = 33.367

    # Sends one command line and returns the reply text.
    def _send(self, line):
        # Turn the command into bytes with a trailing newline.
        data = (line + "\n").encode()
        # Write the command to the Pico.
        self.serial.write(data)
        # Read one line of reply and strip the newline and spaces.
        reply = self.serial.readline().decode().strip()
        return reply

    # Checks that the Pico is connected and responding.
    def ping(self):
        # A healthy Pico replies with PONG.
        return self._send("PING") == "PONG"

    # Rejects button names the firmware does not know about.
    def _check(self, name):
        # Raise a clear error instead of sending a bad command.
        if name not in protocol.BUTTONS:
            raise ValueError("unknown button: " + name)

    # Presses and holds a button.
    def press(self, name):
        self._check(name)
        return self._send("PRESS " + name)

    # Releases a button.
    def release(self, name):
        self._check(name)
        return self._send("RELEASE " + name)

    # Releases every button at once.
    def release_all(self):
        return self._send("RELEASE ALL")

    # Taps a button for a number of milliseconds.
    def tap_ms(self, name, ms):
        self._check(name)
        # The firmware expects a whole number of milliseconds.
        return self._send("TAP " + name + " " + str(int(ms)))

    # Taps a button for a number of game frames.
    # This converts frames to milliseconds using frame_ms.
    def tap_frames(self, name, frames):
        # Work out how long the tap should last in milliseconds.
        ms = frames * self.frame_ms
        return self.tap_ms(name, ms)

    # Closes the serial connection.
    def close(self):
        # Make sure no button is left pressed before we disconnect.
        self.release_all()
        self.serial.close()
