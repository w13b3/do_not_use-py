#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# hsv_sliders.py

try:  # python3
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox
except ImportError:
    raise NotImplemented  # python2

import numpy as np
try:
    import cv2.cv2 as cv
except ImportError:
    import cv2 as cv

from labeled_slider import LabeledSlider


class HSVSliders(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw) -> None:
        super(HSVSliders, self).__init__(master=master, cnf=cnf, **kw)

        # pack configuration
        pack_cnf = {'side': tk.TOP, 'anchor': tk.CENTER, 'fill': tk.X, 'expand': False}
        # Hue low scale
        self.hue_low = LabeledSlider(self, from_=0, to=179, value=0)
        self.hue_low.set_label_text("Hue low:")
        self.hue_low.pack(pack_cnf)
        # Hue high scale
        self.hue_high = LabeledSlider(self, from_=0, to=179, value=179)
        self.hue_high.set_label_text("Hue high:")
        self.hue_high.pack(pack_cnf)
        # Saturation low scale
        self.sat_low = LabeledSlider(self, from_=0, to=255, value=0)
        self.sat_low.set_label_text("Saturation low:")
        self.sat_low.pack(pack_cnf)
        # Saturation high scale
        self.sat_high = LabeledSlider(self, from_=0, to=255, value=255)
        self.sat_high.set_label_text("Saturation high:")
        self.sat_high.pack(pack_cnf)
        # Value low scale
        self.val_low = LabeledSlider(self, from_=0, to=255, value=0)
        self.val_low.set_label_text("Value low:")
        self.val_low.pack(pack_cnf)
        # Value high scale
        self.val_high = LabeledSlider(self, from_=0, to=255, value=255)
        self.val_high.set_label_text("Value high:")
        self.val_high.pack(pack_cnf)

        # Blur scale
        self.blur = LabeledSlider(self, from_=0, to=100, value=0)
        self.blur.set_label_text("Blur:")
        self.blur.pack(pack_cnf)

        self.sliders = {
            "hue_low": self.hue_low,
            "hue_high": self.hue_high,
            "sat_low": self.sat_low,
            "sat_high": self.sat_high,
            "val_low": self.val_low,
            "val_high": self.val_high,
            "blur": self.blur,
        }
        # reset the sliders button
        button_reset = tk.Button(self, text='Reset sliders', bd=3, command=self._reset_button)
        button_reset.event_add("<<RangeChanged>>", "<ButtonRelease>")
        button_reset.pack(pack_cnf)

    def _reset_button(self):
        """ function to reset the sliders back to the values """
        for slider in self.sliders.values():
            slider.reset_scale()  # LabeledSlider function
            slider.update_label_text()  # LabeledSlider function

    def get_masked_frame(self, frame: np.ndarray) -> np.ndarray:
        """ apply the values of the sliders onto the given cv2 array """
        # get the blur scale value
        b_ = int(self.blur.get())
        blur = b_ if b_ % 2 != 0 else b_ + 1  # create uneven value
        # blur the frame
        frame = cv.GaussianBlur(frame, (blur, blur), 0) if blur > 0 else frame
        # convert the color to HSV
        hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Every color except white
        low = np.array([self.hue_low.get(), self.sat_low.get(), self.val_low.get()])
        high = np.array([self.hue_high.get(), self.sat_high.get(), self.val_high.get()])
        mask = cv.inRange(hsv_frame, low, high)
        mask_frame = cv.bitwise_and(frame, frame, mask=mask)
        return mask_frame


if __name__ == '__main__':
    root = tk.Tk()
    root.title("HSV sliders")
    hsv = HSVSliders(root)
    hsv.pack()
    root.mainloop()
