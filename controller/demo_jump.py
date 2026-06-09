# demo_jump.py
# The first milestone for the controller module.
# It makes Crash jump ten times with no video involved.
# If you see Crash jump on screen, the whole input chain works end to end.

import sys
import time
from controller.client import Controller


# Runs the jump demo on the given serial port.
def main(port):
    # Open the connection to the Pico.
    pad = Controller(port)
    # Check the Pico is responding before doing anything.
    if not pad.ping():
        print("Pico did not respond to PING")
        return
    print("Pico connected, jumping ten times")
    # Jump ten times with a short pause between jumps.
    for i in range(10):
        # X is the jump button on Crash, named cross here.
        pad.tap_ms("cross", 80)
        # Wait half a second so the jumps are clearly separate.
        time.sleep(0.5)
        print("jump", i + 1)
    # Clean up the connection and release everything.
    pad.close()
    print("done")


# Read the serial port from the command line and run the demo.
if __name__ == "__main__":
    # Require the port to be passed as an argument.
    if len(sys.argv) != 2:
        print("usage: python -m controller.demo_jump <serial-port>")
    else:
        main(sys.argv[1])
