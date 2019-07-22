#!/usr/bin/python3
import os
import threading
try:
    import tkinter as tk  # sudo apt-get install python3-tk
except ImportError as e:
    print("tkinter is required to run this code\n{0}".format(e))
    exit(1)

class DummyPopup(threading.Thread):
    """ Show a dummy popup

    This shows a dummy popup on the lower right of the screen
    """

    def __init__(self, image):
        image = os.path.realpath(image)
        assert os.path.isfile(image), "image should be a file"
        assert os.path.exists(image), "path to image does not exist"
        assert str(image).lower().endswith((".png", ".jpg", ".gif")), "should give an image format"
        self.image = image
        self.root = None
        threading.Thread.__init__(self)
        self.start()

    def exit_pressed(self, event):
        x, y = event.x, event.y  # get the position of the mouse click
        if 20 < y < 41 and 217 < x < 238:
            # [x] button is pressed on the label image
            self.root.quit()

    def run(self):
        self.root = tk.Tk()  # tkinter as tk
        self.root.overrideredirect(True)  # borderless window
        self.root.attributes('-topmost', True)  # always on top

        # image configs
        img = tk.PhotoImage(master=self.root, file=self.image)
        img_width, img_height = img.width(), img.height()  # get image size's
        x_pos = int(self.root.winfo_screenwidth() - img_width)
        y_pos = int(self.root.winfo_screenheight() - img_height)
        self.root.geometry("{}x{}+{}+{}".format(  # place root it somewhere nice
            int(img_width), int(img_height), int(x_pos), int(y_pos)-40))

        # make a label and place the image on it
        label = tk.Label(self.root, image=img, bd=0)  # create border less image
        label.bind("<Button 1>", self.exit_pressed)  # press the [x] button!
        label.pack()  # show it
        self.root.mainloop()  # loop indefinitely


if __name__ == '__main__':
    DummyPopup(image="popup.png")
