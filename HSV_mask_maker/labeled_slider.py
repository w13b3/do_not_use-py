#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# labeled_slider.py

try:  # python3
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox
except ImportError:
    raise NotImplemented  # python2


class LabeledSlider(tk.Frame):
    """ combined widget that shows a slider with its value above """
    def __init__(self, master=None, from_=0, to=10, value=0, **kw) -> None:
        super(LabeledSlider, self).__init__(master=master)

        # define the scale variable and value
        self._scale_var = kw.pop('variable', False) or tk.IntVar(self, 0)
        self._scale_var.set(value)
        # the default value of the scale
        self._start_val = value
        self._min_val = min(from_, to)
        self._max_val = max(from_, to)

        # set the label
        text = kw.pop('text', '')
        self._label_text = tk.StringVar(self, text)
        self._label = tk.Label(self, cnf={}, **kw)
        self._label.pack(side=tk.TOP, fill=tk.X)
        # update and set the text onto the label
        self.set_label_text(text)

        # bind mouse buttons to the label
        # Left mb to decrease by 1
        # Middle mb to reset
        # right mb to increase by 1
        self._label.bind("<ButtonRelease-1>", lambda e: self._adjust_scale(self._scale_var.get() - 1))
        self._label.bind("<ButtonRelease-2>", lambda e: self._adjust_scale(self._start_val))
        self._label.bind("<ButtonRelease-3>", lambda e: self._adjust_scale(self._scale_var.get() + 1))

        # set the scale
        self._scale = ttk.Scale(self, variable=self._scale_var, from_=from_, to=to)
        self._scale.pack(side=tk.BOTTOM, fill=tk.X)
        self.get = lambda: self._scale_var.get()
        self.set = lambda value: self._scale_var.set(value)
        # add a virtual event and bind it to update the label
        self._scale.event_add("<<RangeChanged>>", '<ButtonRelease>', '<B1-Motion>')
        self._scale.bind("<<RangeChanged>>", self.update_label_text)
        # rebind configuration to scale
        self.configure = self._scale.configure

    def _adjust_scale(self, value):
        """ adjust the scale if value is between the range of the scale """
        if self._min_val <= value <= self._max_val:
            self._scale_var.set(value)
        self.update_label_text()

    def set_label_text(self, text: str) -> None:
        """ set the text to the label """
        self._label_text.set(text)
        self.update_label_text()

    def reset_scale(self) -> None:
        """ reset the scale to it's start value """
        self._scale.set(self._start_val)

    def update_label_text(self, event=None) -> None:
        """ update the label's text """
        # get and create variables
        text_var = self._label_text.get()
        scale_var = self._scale_var.get()
        text = "{0} {1}".format(text_var, scale_var)
        # set the text to the label
        self._label.configure(text=text)


if __name__ == '__main__':
    root = tk.Tk()
    labelslider = LabeledSlider(root, value=5)
    labelslider.set_label_text('custom text, slider value ->')
    labelslider.pack()
    root.mainloop()
