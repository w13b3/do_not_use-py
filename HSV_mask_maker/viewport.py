#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# viewport.py

import sys

try:  # python3
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox
except ImportError:
    raise NotImplemented  # python2


class Viewport(tk.Toplevel):
    """ class that creates a new window """

    def __init__(self, master=None, cnf={}, **kw) -> None:
        super(Viewport, self).__init__(master=master, cnf=cnf, **kw)

        self.title('Viewport')
        self.configure(padx=3, pady=3)
        # self.geometry("300x300")  # initial size
        self.protocol('WM_DELETE_WINDOW', self.__stop)

        self.port = tk.Label(self, bg='white')
        self.port.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

        # create a transparent window
        platform = str(sys.platform).lower()
        if platform == 'win32':  # make window transparent
            self.wm_attributes("-transparentcolor", self.port['bg'])
        elif platform == 'linux':
            self.wm_attributes('-type', 'normal')  # normal window type

        # drag the window by the body
        self._offsetx, self._offsety = 0, 0
        self.bind('<Button-1>', self.__click_window)
        self.bind('<B1-Motion>', self.__drag_window)

    def __click_window(self, event) -> None:
        """ get the current x and y values of the mouse """
        self._offsetx = event.x
        self._offsety = event.y

    def __drag_window(self, event) -> None:
        """ drag window action """
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry(f'+{x}+{y}')

    def __stop(self) -> None:
        """ close button pressed on viewport """
        if messagebox.askokcancel(title="Quit", message="Do you want to quit?"):
            self.destroy()         # remove Viewport
            self.master.destroy()  # destroy the Master also


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry("300x300")
    vp = Viewport(root)
    vp.geometry("300x300")

    if str(sys.platform).lower() == 'linux':
        scale_var = tk.IntVar(root)
        scale = ttk.Scale(root, from_=0, to=100, variable=scale_var)
        # on linux the wm_attributes -transparentcolor doesn't work
        # create a slider for the window transparency
        cmd_ = lambda *e: vp.attributes("-alpha", (scale_var.get() / 100))
        scale.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)
        scale.configure(command=cmd_)

    cmd_ = lambda *e: print(f"{vp.port.winfo_geometry()}\n{vp.winfo_geometry()}")
    root.bind('<ButtonPress>', cmd_)

    root.mainloop()
