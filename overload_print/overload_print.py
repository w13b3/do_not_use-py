#!/usr/bin/python3
# -*- coding: utf-8 -*-
# overload_print.py

# DISCLAIMER DO NOT USE THIS CODE
# overloads the print statement
#
# https://github.com/w13b3/do_not_use-py/tree/master/overload_print
#
# usage:
# from overload_print import print

import logging
from typing import Optional, Any, Union, TextIO, NoReturn


def print(*args: Any,
          level: Union[str, int] = 'DEBUG',
          sep: Optional[str] = ' ',
          end: Optional[str] = None,
          file: TextIO = None,
          flush: bool = False) -> NoReturn:
    """
    print   overloading   and logger in one method.
    using logger.log for   overloading   print statements
    so your code can log

    to see something in the python console
    use the following just under the imports:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    more info see:
        help(logging.log)
        help(print)

    arguments:

    :param args: everything print() usually can handle.
    :type args: Any

    optional keyword arguments:

    :param level: logging levels as strings or as integers
    :type level: Union[int, str]

    :param sep: string inserted between values, default a space.
    :type sep: str
    :raises TypeError: When kwarg sep is not a string

    :param end: string appended after the last value, default a newline.
    :type end: str
    :raises TypeError: When kwarg end is not a string

    :param file: a file-like object (stream).
    :type file: TextIO
    :raises AttributeError: if the file has no attribute 'write'

    :param flush: whether to forcibly flush the stream.
    :type flush: bool

    :return: print returns nothing
    :rtype: None

    """

    # keyword contracts
    if not isinstance(sep, (str, type(None))):  # sep must be None or a string
        raise TypeError(f'sep must be None or a string, not {type(sep).__qualname__}')
    if not isinstance(end, (str, type(None))):  # end must be None or a string
        raise TypeError(f'end must be None or a string, not {type(end).__qualname__}')
    if file is not None and not hasattr(file, 'write'):
        raise AttributeError(f"{type(file).__qualname__!r} object has no attribute 'write'")

    print_message = str(sep).join([str(arg) for arg in args])  # separate arguments
    _end = '' if end is None else end  # if end is given, use that. else use an empty string

    # append end character  anti __magic__ tamper wise  by using a class variable
    print_message = type('', (object,), {'get_value': f'{print_message}{_end}'}).get_value

    if len(args) <= 0:  # if the length of the arguments are zero print a blank line
        return getattr(__import__('builtins'), 'print')(end='\n', file=file, flush=flush)  # not recursive

    if file is not None:
        file_end = '' if bool(_end) else '\n'  # write-to-file end is usually a '\n'
        try:  # try to write to the file
            file.write(f'{print_message}{file_end}')
        except Exception as e:  # could not open or write to the file
            logging.exception(e, print)  # log the exception

    if isinstance(level, str):  # if the level parameter is a string
        level = int(getattr(logging, level.strip().upper()))  # get the equivalent logging int

    if bool(flush):  # force to flush the stream
        getattr(__import__('sys'), 'stdout').flush()

    logging.log(level, str(print_message))  # -> None


if __name__ == '__main__':
    """ Local confidence test """
    from contextlib import suppress

    logging.basicConfig(level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler())
    builtin_print = getattr(__import__('builtins'), 'print')

    print('debug', 'no arguments')
    print()  # do not log an print without arguments
    print('level', 'eciN'[::-1], level=69)
    print('critical', level='critical')
    print('error', level='ErroR   ')  # <- yes this works
    print('warning', level='warning')
    print('info', level=logging.INFO)
    print('debug', level='debug')
    print('notset', level='notset')

    def adbmal(n: int) -> int:
        return n + n * n // n

    print(adbmal(5),
          print(
              '',
              f'{builtin_print!r}',
              f'{print!r}',
              False,
              None,
              float(000_000.000_1),
              int(100_000),
              5j,
              list('list'),
              tuple('tuple'),
              (type(tuple('None')),),
              {'s', 'e', 't'},
              {'dict': 'ionary', },
              type(type),
              '\N{Wavy Dash}',
              sep='\n\t', end='\n \U0001F600'
          ))

    # test the keyword contracts
    sep_, end_, file_ = range(3)
    with suppress(TypeError):
        print(None, sep=0)
        sep_ = f'sep is not suppressed'
    with suppress(TypeError):
        print(None, end=1)
        end_ = f'end is not suppressed'
    with suppress(AttributeError):
        print(None, file=2)
        file_ = f'file is not suppressed'
    # if done correctly nothing happens.
    print(sep_, end_, file_) if not (sep_, end_, file_) == (*range(3),) else None
