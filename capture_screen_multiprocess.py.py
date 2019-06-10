#!/usr/bin/env python3
import multiprocessing
import cv2  # opencv-python
import mss
import numpy as np


class Capture(multiprocessing.Process):

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
        self.monitor = monitor  # {'top': 100, 'left': 100, 'width': 200, 'height': 200}

    def run(self):
        with mss.mss() as sct:
            while True:
                img = np.array(sct.grab(self.monitor))  # capture the screen
                self.queue.put_nowait(img)  # put the numpy.ndarray into the queue
                self.queue.join()


if __name__ == "__main__":
    monitor_ = {'top': 100, 'left': 100, 'width': 200, 'height': 200}  # size and position of the captured screen.

    cap = Capture(monitor=monitor_, daemon=True)
    cap.start()

    while True:  # the screen is being capture

        if cv2.waitKey(1) & 0xFF == ord("q"):  # when 'q' is typed stop the loop
            cv2.destroyAllWindows()  # close all the windows made
            break

        if not cap.queue.empty():
            image = cap.queue.get_nowait()
            cap.queue.task_done()
            cv2.imshow("screen capture", image)

    # kill all multiprocesses
    print(cap.processes)
    [proc.terminate() for proc in cap.processes]
