#!/usr/bin/env python3
import multiprocessing
import cv2  # opencv-python
import mss
import numpy as np


class Capture(multiprocessing.Process):
    """ Capture the screen

    Little code snippet below showing how to use this class:

    import multiprocessing
    import cv2  # opencv-python
    import mss
    import numpy as np

    ...

    if __name__ == "__main__":
        monitor = {'top': 100, 'left': 100, 'width': 200, 'height': 200}  # size and position of the captured screen.

        cap = Capture(monitor=monitor, daemon=True)  # <- daemon process
        cap.start()  # start the process

        while True:  # the screen is being capture
            if cv2.waitKey(1) & 0xFF == ord("q"):  # when 'q' is typed stop the loop
                cv2.destroyAllWindows()  # close all the windows made
                break
            if not cap.queue.empty():  # if the queue is not empty
                image = cap.queue.get_nowait()  # get a frame
                cap.queue.task_done()  # tell the queue that the frame is received
                cv2.imshow("screen capture", image)  # show the frame

        [proc.terminate() for proc in cap.processes]  # terminate all multiprocesses
    """
    queue = multiprocessing.JoinableQueue
    processes = set()

    def __new__(cls, *args, **kwargs):
        # create instance and paste it into processes
        instance = super(__class__, cls).__new__(cls)
        cls.processes.add(instance)  # add instances to the class
        cls.queue = multiprocessing.JoinableQueue()  # every instance it's own queue
        return instance

    def __init__(self, monitor, *args, **kwargs):
        super(Capture, self).__init__(*args, **kwargs)
        assert isinstance(monitor, dict), "monitor needs to be a type(dict)"
        assert {"top", "left", "height", "width"} <= set(monitor), "missing keys in monitor dict"
        self.monitor = monitor  # e.g. {'top': 100, 'left': 100, 'width': 200, 'height': 200}

    def run(self):
        with mss.mss() as sct:
            while True:
                img = np.array(sct.grab(self.monitor))  # capture the screen
                self.queue.put_nowait(img)  # put the numpy.ndarray into the queue
                self.queue.join()


if __name__ == "__main__":
    monitor = {'top': 100, 'left': 100, 'width': 200, 'height': 200}  # size and position of the captured screen.

    cap = Capture(monitor=monitor, daemon=True)  # <- deamon process
    cap.start()  # start the process

    while True:  # the screen is being capture
        if cv2.waitKey(1) & 0xFF == ord("q"):  # when 'q' is typed stop the loop
            cv2.destroyAllWindows()  # close all the windows made
            break
        if not cap.queue.empty():  # if the queue is not empty
            image = cap.queue.get_nowait()  # get a frame
            cap.queue.task_done()  # tell the queue that the frame is received
            cv2.imshow("screen capture", image)  # show the frame

    [proc.terminate() for proc in cap.processes]  # terminate all multiprocesses
