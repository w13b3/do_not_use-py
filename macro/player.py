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
        logging.error(f'file not found. path given: {record_file_path}')
        exit(1)
    except Exception as err:
        logging.exception('a general exception has occurred!')
        exit(1)
    else:
        line_generator = filter(None, (line.strip() for line in lines.split('\n')))
        return line_generator


def start_input_player(record_file_path: str) -> None:
    """
    plays the given recorded file that is recorded by record.py

    :param record_file_path: a path to the file that is made by record.py
    """
    generator = _read_record_file(record_file_path)
    time_start, time_end, time_between = 0, 0, 0
    player_instance = _Player()

    with keyboard.Listener(on_release=_stop_player):
        for line in generator:
            if STOP_LISTEN:  # changed to True by _stop_player
                logging.info(f'{STOP_KEY} is pressed, stopping the player!')
                break

            # split the line in the record log made by record.py
            logged_time, function, *arguments = line.split(':')

            # set the wait between lines
            time_start = float(logged_time)
            if bool(time_end):
                time_between = time_start - time_end
            time.sleep(time_between)
            time_end = time_start

            logging.debug(f"time_between {time_between}")
            logging.debug(f"time_start {time_start}")
            logging.debug(f"time_end {time_end}")
            logging.debug(f"function {function}")
            logging.debug(f"arguments {arguments}")
            logging.debug(f"current line: {line}")

            getattr(player_instance, function)(*arguments)


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

        evaluated_action = _action
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
        logging.debug(f'mouse_controller.position = ({x}, {y})')
        self.mouse_controller.position = (int(x), int(y))

    def mouse_scroll(self, dx: int, dy: int, *args, **kwargs) -> None:
        """
        makes the mouse scroll

        :param dx: horizontal scroll direction
        :param dy: vertical scroll direction
        :param args: catch for other arguments
        :param kwargs: catch for other keywords
        """
        logging.debug(f'mouse_scroll({dx}, {dy})')
        self.mouse_controller.scroll(dx=int(dx), dy=int(dy))

    def mouse_click(self, button: (Button, str), action: (bool, str), *args, **kwargs) -> None:
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
        logging.debug(f'keyboard_key({button}, {action})')

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
        logging.debug(f'keyboard_key({key}, {action})')


if __name__ == '__main__':
    print("start\n")

    file = '/tmp/record_main.txt'
    start_input_player(file)
