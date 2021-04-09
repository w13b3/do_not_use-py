#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cv_hsv_trackbars.py

import colorsys
from types import SimpleNamespace

import cv2
import cv2.cv2 as cv
import numpy as np


class HSVTrackbars:

    def __init__(self) -> None:
        self.tolerance = 5
        self.window_name = 'HSV - control'
        # could replace SimpleNamespace with dict
        self.hue_low = SimpleNamespace(name='Hue low', default=0, min=0, max=179, current=0)
        self.hue_high = SimpleNamespace(name='Hue high', default=179, min=0, max=179, current=179)
        self.sat_low = SimpleNamespace(name='Sat low', default=0, min=0, max=255, current=0)
        self.sat_high = SimpleNamespace(name='Sat high', default=255, min=0, max=255, current=255)
        self.val_low = SimpleNamespace(name='Val low', default=0, min=0, max=255, current=0)
        self.val_high = SimpleNamespace(name='Val high', default=255, min=0, max=255, current=0)
        self.blur = SimpleNamespace(name='Blur', default=0, min=0, max=100, current=0)
        self.bars = (self.hue_low, self.hue_high, self.sat_low, self.sat_high, self.val_low, self.val_high, self.blur)
        self.__create_window()
        self.__reset_trackbar_values(cv.EVENT_LBUTTONUP)  # hack
        self.__update_trackbar_values()

    def __create_window(self) -> None:
        """ create a window with trackbars and a `button` to reset the trackbars """
        cv.namedWindow(self.window_name, cv.WINDOW_GUI_NORMAL)
        # create a `button`
        blanco = 255 * np.ones(shape=[50, 250, 3], dtype=np.uint8)
        cv.putText(blanco, 'click to reset', (15, 35), cv.QT_FONT_NORMAL, 1, (0, 0, 0))
        # apply the button onto the canvas
        cv.imshow(self.window_name, blanco)
        # perform an action when clicked on the `button`
        cv.setMouseCallback(self.window_name, self.__reset_trackbar_values)
        # create the trackbars to the window
        for bar in self.bars:
            cv.createTrackbar(bar.name, self.window_name, bar.min, bar.max, self.__update_trackbar_values)

    def __update_trackbar_values(self, event=None, *args) -> None:
        """ update all the values of the trackbars """
        for bar in self.bars:
            bar.current = cv.getTrackbarPos(bar.name, self.window_name)

    def __reset_trackbar_values(self, event=None, *args) -> None:
        """ when clicked on the `button` reset all the trackbars """
        if event == cv.EVENT_LBUTTONUP:
            for bar in self.bars:  # set all to default
                bar.current = cv.setTrackbarPos(bar.name, self.window_name, bar.default)
            self.__update_trackbar_values()

    def set_trackbars(self, b, g, r) -> None:
        """ set the given trackbars to the given rgb value """
        h_f, s_f, v_f = colorsys.rgb_to_hsv(r, g, b)
        h_val, s_val, v_val = int(h_f * 179), int(s_f * 255), int(v_f)
        cv.setTrackbarPos(self.hue_high.name, self.window_name, h_val + self.tolerance)
        cv.setTrackbarPos(self.hue_low.name, self.window_name,  h_val - self.tolerance)
        cv.setTrackbarPos(self.sat_high.name, self.window_name, s_val + self.tolerance)
        cv.setTrackbarPos(self.sat_low.name, self.window_name,  s_val - self.tolerance)
        cv.setTrackbarPos(self.val_high.name, self.window_name, v_val + self.tolerance)
        cv.setTrackbarPos(self.val_low.name, self.window_name,  v_val - self.tolerance)
        self.__update_trackbar_values()

    def blur_image(self, src: np.ndarray) -> np.ndarray:
        """ add a simple gaussian blur on the image """
        k = int(self.blur.current)
        k = k if k % 2 != 0 else k + 1  # make sure the k is uneven
        src = cv2.GaussianBlur(src, (k, k), 0)
        return src

    def apply_hsv(self, src: np.ndarray) -> np.ndarray:
        """ apply the sliders on a given image """
        # apply the blur slider before the HSV sliders
        src = self.blur_image(src)
        # apply the HSV sliders
        hsv_img = cv.cvtColor(src, cv.COLOR_BGR2HSV)
        hsv_low = np.array([self.hue_low.current, self.sat_low.current, self.val_low.current], np.uint8)
        hsv_high = np.array([self.hue_high.current, self.sat_high.current, self.val_high.current], np.uint8)
        mask = cv.inRange(hsv_img, hsv_low, hsv_high)
        src = cv.bitwise_and(src, src, mask=mask)
        return src


if __name__ == '__main__':
    def get_color(x: int, y: int, img: np.ndarray) -> (int, int, int):
        """ retrieve the b r g color values from the given image """
        b, g, r, *_ = map(int, (*img[y, x],))  # change to int
        return b, g, r

    def on_click(event, x, y, flags, params):
        """ when the image is clicked, set the hsv trackbars """
        if event == cv.EVENT_LBUTTONUP:
            b, g, r = get_color(x, y, params)
            hsv.set_trackbars(b, g, r)

    # make a resizable window
    window_name = 'Image'
    cv.namedWindow(window_name, cv.WINDOW_GUI_NORMAL)

    image_file = "/some/path/to/image.png"  # <- path to local image here

    # create the window with the trackbars
    hsv = HSVTrackbars()
    hsv.tolerance = 5

    while bool(cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE)):
        try:
            img = cv.imread(image_file)
            img = hsv.apply_hsv(img)

            # show the image
            cv.imshow(window_name, img)
            # click on the image to set the hsv values
            cv.setMouseCallback(window_name, on_click, img)

            if cv.waitKey(1) & 0xFF == ord("q"):
                break  # if Q is pressed
        except KeyboardInterrupt:
            break

    # clean up
    cv.destroyAllWindows()
