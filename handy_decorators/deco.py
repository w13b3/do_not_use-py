#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# deco.py

import functools


def capitalize_words(func: callable) -> callable:
    """ Makes Every Word In A Sentence Start With A Capital Letter """
    from string import capwords

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        args = [capwords(val) if isinstance(val, str) else val for val in args]
        kwargs = {key: capwords(val) if isinstance(val, str) else val for key, val in kwargs.items()}
        return func(*args, **kwargs)
    return inner_func


def clapping_hands(func: callable) -> callable:
    """ Makes every whitespace a clapping hands emoji """
    import string  # for available whitespaces
    whitespace = string.whitespace.replace('\n\r', '')  # ignore newlines
    claps = "\N{Clapping Hands Sign}"  # https://www.fileformat.info/info/unicode/char/1f44f/index.htm
    replace = functools.lru_cache()(lambda val: ''.join([c.replace(c, claps) if c in whitespace else c for c in val]))

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        args = [replace(val) if isinstance(val, str) else val for val in args]
        kwargs = {key: replace(val) if isinstance(val, str) else val for key, val in kwargs.items()}
        return func(*args, **kwargs)
    return inner_func


if __name__ == '__main__':

    # @capitalize_words
    # @clapping_hands
    # def func(x): return x

    def func(x): return x
    call_me = clapping_hands(func)  # are you scared of decorators?
    cap_words = capitalize_words(func)

    print(call_me('This\fsentence\vwhitespace\tare clapping hands emoji\'s'))
    print(call_me(x='A keyword?\nA new line!\nAre you serious right now\N{INTERROBANG}'))
    print(call_me(cap_words('Are you serious right now\N{INTERROBANG}')))
