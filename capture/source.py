# source.py
# The frame source interface for the capture module.
# Every capture device we support provides frames through this same interface.
# Swapping the Elgato for the PiKVM later just means a new class with these methods.


# Base class that all frame sources follow.
class FrameSource:
    # Returns the most recent frame as a numpy array in BGR color order.
    # Returns None if no frame is available.
    def get_frame(self):
        raise NotImplementedError

    # Releases the device and any resources it holds.
    def close(self):
        raise NotImplementedError
