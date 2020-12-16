#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# player.py

import time
import logging
import pathlib

from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode

STOP_LISTEN = False  # changed by _stop_player
STOP_KEY = Key.esc


def _stop_player(key: Key) -> None:
    """ pynput.keyboard.Listener on_release """
    global STOP_LISTEN  # get global variable inside the function enable it to change it
    if key == STOP_KEY:
        STOP_LISTEN = True


def _read_record_file(record_file_path: str) -> iter:
    """ read a recorded file """
    try:
        lines = pathlib.Path(record_file_path).read_text()
    except FileNotFoundError as err:
        logging.error(f"file not found. path given: {record_file_path}")
        exit(1)
    except Exception as err:
        logging.exception("a general exception has occurred!")
        exit(2)
    else:
        line_generator = filter(None, (line.strip() for line in lines.split("\n")))
        return line_generator


def start_input_player(record_file_path: str) -> None:
    """
    plays the given recorded file that is recorded by record.py

    :param record_file_path: a path to the file that is made by record.py
    """
    generator = _read_record_file(record_file_path)
    time_start, time_end, time_between = 0, 0, 0
    player_instance = _Player()
    # filter out the functions that are not used
    play_functions = tuple(filter(lambda f_: not f_.startswith("_"), dir(player_instance)))

    exit_code = 0
    with keyboard.Listener(on_release=_stop_player):
        for step, line in enumerate(generator, start=1):
            if STOP_LISTEN:  # changed to True by _stop_player
                logging.info(f"{STOP_KEY} is pressed, stopping the player!")
                exit_code = 1
                break

            logging.info(f"step: {step}")

            try:  # split the line in the record log made by record.py
                logged_time, function, *arguments = line.split(":")
            except ValueError:
                logging.error(f"could not unpack line: {line}")
                continue  # next in for-loop

            # set the wait between lines
            time_start = float(logged_time)
            if bool(time_end):
                time_between = time_start - time_end
            time.sleep(time_between)  # wait between actions
            time_end = time_start

            logging.debug(f"time_between {time_between}")
            logging.debug(f"time_start {time_start}")
            logging.debug(f"time_end {time_end}")
            logging.debug(f"function {function}")
            logging.debug(f"arguments {arguments}")
            logging.debug(f"current line: {line}")

            if function == "END_RECORD":  # default use "END_RECORD"
                logging.debug(f"end of file: {record_file_path}")
                exit(exit_code)  # exit_code = 0

            if function not in play_functions:
                logging.debug(f"function not available: {function}")
                continue  # next in for-loop

            # call _Player().function(*arguments)
            getattr(player_instance, function)(*arguments)

        # make sure the code stops
        exit(exit_code)


class _Player:
    """ class used by start_input_player to control the mouse and keyboard """

    # pynput objects to control the mouse and keyboard
    mouse_controller = mouse.Controller()
    keyboard_controller = keyboard.Controller()

    @staticmethod
    def _evaluate(_input: str, _action: str) -> (object, int):
        """ evaluate the input and action """

        evaluated_input = _input
        if isinstance(_input, str):  # if action is type: bool, do nothing
            evaluated_input = eval(_input)

        evaluated_action = _action or "0"
        if isinstance(_action, str):  # if action is type: bool, do nothing
            evaluated_action = bool(eval(_action))

        return evaluated_input, evaluated_action

    def mouse_move(self, x: int, y: int, *args, **kwargs) -> None:
        """
        makes the mouse move

        :param x: pixel position on the screen
        :param y: pixel position on the screen
        :param args: catch for other arguments
        :param kwargs: catch for other keywords
        """
        logging.debug(f"mouse_controller.position = ({x}, {y})")
        self.mouse_controller.position = (int(x), int(y))

    def mouse_scroll(self, dx: int, dy: int, *args, **kwargs) -> None:
        """
        makes the mouse scroll

        :param dx: horizontal scroll direction
        :param dy: vertical scroll direction
        :param args: catch for other arguments
        :param kwargs: catch for other keywords
        """
        logging.debug(f"mouse_scroll({dx}, {dy})")
        self.mouse_controller.scroll(dx=int(dx), dy=int(dy))

    def mouse_click(self, button: (Button, str), action: (bool, str) = False, *args, **kwargs) -> None:
        """
        makes the mouse press or release the mousebutton on the position where it is located

        :param button: represents the mouse.Button in string or mouse.Button object
        :param action: represents a True or False value. True is button press, False is button release
        :param args: catch for other arguments
        :param kwargs: catch for other keywords
        """
        key_button, press_or_release = self._evaluate(button, action)
        button_event = self.mouse_controller.release
        if bool(press_or_release):
            button_event = self.mouse_controller.press

        button_event(key_button)
        logging.debug(f"keyboard_key({button}, {action})")

    def keyboard_key(self, key: (Key, str), action: (bool, str), *args, **kwargs) -> None:
        """
        presses or releases a key on the keyboard

        :param key: represents the keyboard.Key in string or keyboard.Key  object
        :param action: represents a True or False value. True is key press, False is key release
        :param args: catch for other arguments
        :param kwargs: catch for other keywords
        """
        key_button, press_or_release = self._evaluate(key, action)
        button_event = self.keyboard_controller.release
        if bool(press_or_release):
            button_event = self.keyboard_controller.press

        button_event(key_button)
        logging.debug(f"keyboard_key({key}, {action})")


if __name__ == '__main__':
    from tempfile import gettempdir
    print("start\n")

    logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    modified_time = 0
    record_file = None
    if not bool(record_file):
        # find temp file made by record.py -> start_input_record(None)
        for temp_file in pathlib.Path(gettempdir()).iterdir():
            name = str(temp_file.name)

            if name.startswith("input_record_") and name.endswith("_.txt"):
                mtime = temp_file.stat().st_mtime  # get the latest modified file
                if mtime > modified_time:
                    modified_time = mtime
                    record_file = str(temp_file)

    # start player
    start_input_player(record_file)