#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# capture_screen_multiprocess.py

import logging
from queue import Full, Empty
from multiprocessing import Process, Queue, Array, set_start_method

import mss
import mss.tools
from mss.screenshot import ScreenShot
from mss import ScreenShotError

import numpy as np


class ScreenCapture(Process):

    def __init__(self, queue: Queue, bbox: Array):
        super(ScreenCapture, self).__init__(daemon=True)
        self._queue = queue
        self.bbox = bbox
        self._running = True

    def run(self) -> None:
        """ starts when ScreenCapture.start() is called """
        logging.info(f"{self.name} start process")
        self.__start_screen_capture()

    def stop(self) -> None:
        """ stop the screen capture """
        logging.info(f"{self.name} stop process")
        self._running = not bool(self._running)
        self.terminate()  # stop the process
        self.join(timeout=5)  # join with the main

    def __start_screen_capture(self) -> None:
        """ loop that puts the screenshot made into the queue """
        with mss.mss() as sct:
            logging.debug(f"{self.name} start screen capture: {self._running}")
            while self._running:
                try:
                    area = (*self.bbox[:],)                 # PIL bbox tuple
                    img_grab: ScreenShot = sct.grab(area)   # make a screenshot
                    np_arr = np.asarray(img_grab)           # convert to np.ndarray
                    self._queue.put(np_arr, timeout=0.01)   # put it in the queue
                except ScreenShotError:
                    msg = f"{self.name}, ScreenShotError bbox: {area}"
                    logging.exception(msg)
                    break
                except KeyboardInterrupt:
                    msg = f"{self.name}, KeyboardInterrupt"
                    logging.exception(msg)
                    break
                except Full:  # when the queue is full, ignore it
                    continue  # next loop


if __name__ == "__main__":
    """ mirror the image of the Viewport onto the Porthole """
    try:
        # opencv-python
        import cv2.cv2 as cv
    except ImportError:
        import cv2 as cv

    # create the Viewport window
    viewport = 'Viewport'
    cv.namedWindow(viewport, cv.WINDOW_GUI_NORMAL)
    cv.setWindowProperty(viewport, cv.WND_PROP_AUTOSIZE, cv.WINDOW_NORMAL)
    cv.setWindowProperty(viewport, cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_FREERATIO)

    set_start_method('spawn')  # windows default

    img_queue = Queue(maxsize=3)  # always up to date with a buffer of 3 frames
    # shared memory array with 4 places (left, upper, right, lower)
    monitor = Array('i', (1, 1, 2, 2))

    # start making screenshots
    screen_capture = ScreenCapture(img_queue, monitor)
    screen_capture.start()

    # use mss to get the width and height of the monitor(s)
    mon: dict = mss.mss().monitors[0]
    mon_width = mon.get('width')
    mon_height = mon.get('height')

    while screen_capture.is_alive():
        try:
            # get the image from the queue that is put in by ScreenCapture
            img = img_queue.get_nowait()
            # show the image in the Porthole
            cv.imshow('Porthole', img)

            # get the location of the black square on the Viewport window
            w_left, w_top, w_width, w_height = cv.getWindowImageRect(viewport)
            # Convert PIL bbox style (left, upper, right, lower)
            left, upper, right, lower = w_left, w_top, (w_left + w_width), (w_top + w_height)
            # make sure the window never gets out of the screen
            left = left if 0 <= left else 0
            upper = upper if 0 <= upper else 0
            right = right if right < mon_width else mon_width
            lower = lower if lower < mon_height else mon_height
            # set it to the monitor array so the ScreenCapture process can use it
            monitor[:] = (left, upper, right, lower)

            if not bool(cv.getWindowProperty(viewport, cv.WND_PROP_VISIBLE)):
                break  # if the Viewport is closed
            if cv.waitKey(1) & 0xFF == ord("q"):
                break  # if Q is pressed
        except Empty:
            continue
        except KeyboardInterrupt:
            break

    # clean up
    cv.destroyAllWindows()
    screen_capture.stop()
    screen_capture.join()
