#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scrollbar.py

try:  # python3
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    raise NotImplemented  # python2


class Scrollbar(tk.Scrollbar):
    """ generic scrollbar widget that packs itself on the given master widget """
    def __init__(self, master=None, orient=tk.HORIZONTAL) -> None:
        if orient not in {tk.HORIZONTAL, tk.VERTICAL}:
            msg = "orient is expected to be 'horizontal' or 'vertical'"
            raise ValueError(msg)

        if not hasattr(master, 'xview') or not hasattr(master, 'yview'):
            msg = "master should have the attribute 'xview' or/and 'yview'"
            raise AttributeError(msg)

        super(Scrollbar, self).__init__(master=master, orient=orient)
        if orient == tk.HORIZONTAL:
            # mouse scroll-wheel to scroll
            self.pack(side=tk.BOTTOM, fill=tk.X)
            self.configure(command=master.xview)
            master.configure(xscrollcommand=self.set)
        else:  # orient == tk.VERTICAL
            # shift-key + mouse scroll-wheel to scroll
            self.pack(side=tk.RIGHT, fill=tk.Y)
            self.configure(command=master.yview)
            master.configure(yscrollcommand=self.set)


if __name__ == '__main__':
    import string
    import random

    # start a window
    root = tk.Tk()
    root.title('Scrollbar test')
    root.geometry("300x100")
    root.configure(padx=10, pady=10)

    # create a text widget
    text = tk.Text(root, wrap='none')
    text.pack(fill=tk.BOTH, expand=True)

    # add the scrollbars to the text widget
    Scrollbar(text, tk.HORIZONTAL)
    Scrollbar(text, tk.VERTICAL)

    def insert_text():
        # insert some random characters
        text.insert(tk.END, random.choice(string.printable))
        if not len(text.get(1.0, "end-1c")) == 2000:
            print(text.winfo_width(), text.winfo_height())
            print(root.winfo_width())
            root.after(10, insert_text)

    # call the looping function
    insert_text()

    # loop the tkinter window
    root.mainloop()
