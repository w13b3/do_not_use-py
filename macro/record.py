#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# record.py

import logging
from tempfile import NamedTemporaryFile

from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode


STOP_LISTEN = False  # changed by _on_release
STOP_KEY = Key.esc
MOUSE_BUTTON = False  # enable dragging


def start_input_record(record_file_path: str = None) -> str:
    """
    listens to all the inputs made by the user and records them.

    :param record_file_path: if given, this file-path is used to create (overwrite) the file.
    :return: recorded file path
    """
    if not bool(record_file_path):
        temp_file = NamedTemporaryFile(mode='w', delete=False, prefix='input_record_', suffix='.txt')
        record_file_path = temp_file.name

    # misuse the python logging module to create a record
    logging.basicConfig(level=logging.DEBUG, filemode='w', filename=record_file_path,
                        format='%(created)s:%(message)s')

    mouse_listener = mouse.Listener(
        on_move=_on_move,
        on_click=_on_click,
        on_scroll=_on_scroll)

    keyboard_listener = keyboard.Listener(
        on_press=_on_press,
        on_release=_on_release)

    mouse_listener.start()
    keyboard_listener.start()

    while not STOP_LISTEN:
        pass

    return record_file_path


def _on_move(x: int, y: int) -> str:
    """ pynput.mouse.Listener on_move """
    msg = f'mouse_move:{x}:{y}'
    if MOUSE_BUTTON:  # enable dragging
        logging.debug(f'mouse_move:{x}:{y}')  # uncomment to record the mouse movement
    return msg


def _on_click(x: int, y: int, button: Button, action: bool) -> str:
    """ pynput.mouse.Listener on_click """
    global MOUSE_BUTTON
    MOUSE_BUTTON = action  # enable dragging

    msg = f'mouse_move:{x}:{y}'
    logging.debug(msg)

    # key presses are send as 0 or 1, create same behaviour with int(bool)
    msg = f'mouse_click:{button}:{int(action)}'
    logging.debug(msg)
    return msg


def _on_scroll(x: int, y: int, dx: int, dy: int) -> str:
    """ pynput.mouse.Listener on_scroll """
    if bool(dy):
        msg = f'mouse_move:{x}:{y}'
        logging.debug(msg)

    msg = f'mouse_scroll:{dx}:{dy}'
    logging.debug(msg)
    return msg


def _on_press(key: Key) -> str:
    """ pynput.keyboard.Listener on_press """
    msg = f'keyboard_key:{key}:'
    if key != STOP_KEY:
        logging.debug(msg)

    return msg


def _on_release(key: Key) -> str:
    """ pynput.keyboard.Listener on_release """
    global STOP_LISTEN  # get global variable inside the function enable it to change it

    msg = f'keyboard_key:{key}:0'
    # stop_key (default  Key.esc) stop the listeners
    if key == STOP_KEY:
        STOP_LISTEN = True
    else:
        logging.debug(msg)

    return msg


if __name__ == '__main__':
    print("start\n")

    file = '/tmp/record_main.txt'
    # file = None
    print(
        start_input_record(file)
    )
