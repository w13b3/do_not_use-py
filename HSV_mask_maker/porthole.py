#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# porthole.py

try:  # python3
    import tkinter as tk
    import tkinter.ttk as ttk
except ImportError:
    raise NotImplemented  # python2

from scrollbar import Scrollbar


class Porthole(tk.Canvas):
    """ canvas widget that shows a image """
    def __init__(self, master=None, cnf={}, scrollbars: bool = True, **kw) -> None:
        super(Porthole, self).__init__(master=master, cnf=cnf, **kw)

        self._image: tk.PhotoImage = tk.PhotoImage(
            name=self.__class__.__qualname__, master=master)
        self._image.blank()
        self._image_data = tk.StringVar(self, b'')

        # add scrollbars to the canvas
        if bool(scrollbars):
            Scrollbar(self, tk.HORIZONTAL)
            Scrollbar(self, tk.VERTICAL)

    def image_size(self) -> (int, int):
        """ get the size of the current image """
        return self._image.width(), self._image.height()

    def clear_image(self) -> None:
        """ clear the canvas of the current image"""
        self._image_data.set(b'')
        self._image.blank()

    def get_rgb_value(self, x, y) -> (int, int, int):
        return self._image.get(x, y)

    def get_image(self) -> bytes:
        """ get the current bytes of the given image on the canvas """
        return self._image_data.get()

    def set_image(self, data: bytes, *, clear_before: bool = True) -> None:
        """ set an image onto the canvas """
        # clear the image
        self.clear_image() if clear_before else None
        self._image_data.set(data)  # remember the current data
        self._image.put(data=data)  # set te image to the PhotoImage
        # add the image to the canvas
        self.create_image(0, 0, image=self._image, anchor=tk.NW)
        # update the scroll region for the scrollbars
        self.configure(scrollregion=(0, 0, *self.image_size()))


if __name__ == '__main__':
    import string
    import base64

    icon = """
    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
    """
    # strip all whitespaces, newlines and tabs
    icon = ''.join(filter(lambda _: _ not in string.whitespace, icon))
    # convert the base64 to bytes
    icon_bytes = base64.b64decode(icon)

    # start a window
    root = tk.Tk()
    root.title('Porthole test')
    root.geometry("200x200")

    # add the Porthole widget
    porthole = Porthole(master=root)
    porthole.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
    # set the icon to the porthole canvas
    porthole.set_image(icon_bytes)
    porthole.bind("<ButtonPress>", lambda e: print(porthole.get_image(), '\n', porthole.image_size()))

    # loop the tkinter window
    root.mainloop()
