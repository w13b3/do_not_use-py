#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# screengrab.py


import sys

try:  # python3
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    raise NotImplemented  # python2

# pypi.org/project/mss/
import mss
import mss.tools
from mss.screenshot import ScreenShot


class ScreenGrab:
    """ class that makes a screenshot of the given tk widget """
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.monitor_size = (self.master.winfo_screenwidth(), self.master.winfo_screenheight())

    def monitor(self) -> dict:
        """ get the window to 'catch', this is the window of the master """
        # split the winfo_geometry
        geosplit = lambda g: (int(_) for _ in str(g).replace("x", " ").replace("+", " ").split(" "))
        window = tuple(geosplit(self.master.winfo_geometry()))
        w_width, w_height, w_left, w_top = window

        # get the monitor resolution
        mon_right, mon_bottom = self.monitor_size

        # assure the window doesn't go outside of the monitors
        # this also prevents mss.error's in linux
        w_top = w_top if 0 < w_top else mon_bottom  # top side
        w_top = w_top if w_top < (mon_bottom - w_height) else int(mon_bottom - w_height)  # bottom side
        w_left = w_left if 0 < w_left else 0  # left side
        w_left = w_left if w_left < (mon_right - w_width) else int(mon_right - w_width)  # right side

        if str(sys.platform).lower() == 'win32':
            # add the offset in windows 10
            w_top = (w_top + 31) + self.master['pady']
            w_left = (w_left + 8) + self.master['padx']
            w_width = (w_width - 3) - self.master['padx']
            w_height = (w_height - 3) - self.master['pady']

        # monitor for mss
        retval = {
            "top": int(w_top), "left": int(w_left),
            "width": int(w_width), "height": int(w_height)
        }
        return retval

    def get_image(self) -> ScreenShot:
        with mss.mss() as sct_:
            return sct_.grab(self.monitor())

    def image_as_png_bytes(self) -> bytes:
        img_: ScreenShot = self.get_image()
        return mss.tools.to_png(img_.rgb, img_.size)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Screengrab test")
    screen_grab = ScreenGrab(root)
    cmd_ = lambda: print(f"{screen_grab.image_as_png_bytes()}\n{screen_grab.monitor()}")
    btn = tk.Button(root, text='print data', command=cmd_)
    btn.pack(anchor=tk.CENTER)
    root.mainloop()