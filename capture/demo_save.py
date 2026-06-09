# demo_save.py
# A simple test for the capture module.
# It grabs frames, saves a few to disk, and prints the measured frame rate.
# Use this to confirm the Elgato is feeding real game video into the program.

import sys
import time
import cv2
from capture.elgato import ElgatoSource


# Runs the capture demo using the given device index.
def main(index):
    # Open the Elgato capture source.
    source = ElgatoSource(index)
    print("capture opened at index", index)
    # Count how many frames we successfully grab.
    count = 0
    # Record the start time so we can work out the frame rate.
    start = time.time()
    # Grab thirty frames.
    for i in range(30):
        # Get the latest frame.
        frame = source.get_frame()
        # Skip and warn if a frame failed to arrive.
        if frame is None:
            print("frame", i, "failed")
            continue
        # Save the first, middle, and last frames so we can look at them.
        if i in (0, 15, 29):
            filename = "frame_" + str(i) + ".png"
            cv2.imwrite(filename, frame)
            print("saved", filename)
        count += 1
    # Work out how long the grabs took.
    elapsed = time.time() - start
    # Avoid dividing by zero if something went very wrong.
    if elapsed > 0:
        print("grabbed", count, "frames in", round(elapsed, 2), "seconds")
        print("about", round(count / elapsed, 1), "frames per second")
    # Release the device.
    source.close()


# Read the device index from the command line and run the demo.
if __name__ == "__main__":
    # Default to index 0 if no argument is given.
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
    else:
        main(0)
