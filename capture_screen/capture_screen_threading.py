#!/usr/bin/env python3
import queue
import threading
import mss
import cv2  # opencv-python
import numpy as np


class Capture(threading.Thread):
    """ Capture the screen

    Little code snippet below showing how to use this class:

    import queue
    import threading
    import mss
    import cv2  # opencv-python
    import numpy as np

    ...

    if __name__ == '__main__':
        monitor = {'top': 100, 'left': 100, 'width': 200, 'height': 200}  # size and position of the captured screen.

        capture_queue = queue.Queue()
        app = Capture(monitor, capture_queue, daemon=True)  # <- daemon thread
        app.start()  # start the thread

        while True:  # the screen is being captured
            cv2.imshow("screen capture", capture_queue.get())  # show the image that is being captured
            if cv2.waitKey(1) & 0xFF == ord('q'):  # when 'q' is typed stop the recording
                cv2.destroyAllWindows()  # close all the windows made
                break  # break the while loop
    """

    def __init__(self, monitor, queue, *args, **kwargs):
        """ Init of Capture

        :param monitor: (dict) containing te top, left coordinates and the height, width of the screen.
        :param _queue: (queue.Queue) a queue to put in the numpy.ndarray
        :param args: (*args) pass on arguments to the Thread class
        :param kwargs: (**kwargs) pass on keyword arguments to the Thread class
        """
        super().__init__(*args, **kwargs)
        assert isinstance(monitor, dict), "monitor needs to be a type(dict)"
        assert {"top", "left", "height", "width"} <= set(monitor), "missing keys in monitor dict"
        self.queue = queue
        self.monitor = monitor  # e.g. {'top': 100, 'left': 100, 'width': 200, 'height': 200}

    def run(self):  # run thread
        # type: (queue) -> None
        """ Override run of the threading.Thread class """
        with mss.mss() as screencapture:
            while True:
                screen = screencapture.grab(self.monitor)  # capture the screen
                self.queue.put(np.array(screen))  # put the numpy.ndarray into the queue


if __name__ == '__main__':
    monitor = {'top': 100, 'left': 100, 'width': 200, 'height': 200}  # size and position of the captured screen.

    capture_queue = queue.Queue()
    app = Capture(monitor, capture_queue, daemon=True)  # <- daemon thread
    app.start()  # start the thread

    while True:  # the screen is being captured
        cv2.imshow("screen capture", capture_queue.get())  # show the image that is being captured
        if cv2.waitKey(1) & 0xFF == ord('q'):  # when 'q' is typed stop the recording
            cv2.destroyAllWindows()  # close all the windows made
            break  # break the while loop
