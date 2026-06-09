# elgato.py
# Frame source for the Elgato HD60 S capture card.
# It uses OpenCV to read frames from the card as if it were a webcam.
# The card must be showing the PlayStation output for this to return game frames.

import cv2
from capture.source import FrameSource


# Reads frames from the Elgato HD60 S using OpenCV.
class ElgatoSource(FrameSource):
    # Opens the capture device at the given index.
    # The index is which video device the system assigns to the Elgato.
    # With only the Elgato connected it is often index 0 or 1.
    def __init__(self, index=0):
        # Remember the index for error messages.
        self.index = index
        # Open the capture device.
        self.cap = cv2.VideoCapture(index)
        # Fail clearly if the device could not be opened.
        if not self.cap.isOpened():
            raise RuntimeError("could not open capture device at index " + str(index))

    # Returns the most recent frame, or None if the read failed.
    def get_frame(self):
        # Grab one frame from the device.
        ok, frame = self.cap.read()
        # Return the frame only if the read succeeded.
        if not ok:
            return None
        return frame

    # Releases the capture device.
    def close(self):
        self.cap.release()
