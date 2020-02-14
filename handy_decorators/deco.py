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


def replace_whitespace(func: callable = None, **options) -> callable:
    """ Replaces whitespace characters with a given replacement
    Default whitespaces are removed and replaced by nothing: ''

    :param func: the function that got decorated
    :type func: callable
    :param whitespace: (optional) what you consider a whitespace
    :type whitespace: str
    :param replacement: (optional) replace the whitespace with given string
    :type replacement: str
    :param r: (optional) replace the whitespace with given string
    :type r: str
    :return: the decorated function
    :rtype: callable
    """
    import string  # for available whitespaces
    whitespace = options.get('whitespace', False) or string.whitespace.replace('\n\r', '')  # ignore newlines
    if func is not None:
        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            new_ws = options.get('replacement', False) or options.get('r', '')
            replace = functools.lru_cache()(  # cache the replacement
                lambda val: ''.join([c.replace(c, new_ws) if c in whitespace else c for c in val]))
            args = [replace(val) if isinstance(val, str) else val for val in args]
            kwargs = {key: replace(val) if isinstance(val, str) else val for key, val in kwargs.items()}
            return func(*args, **kwargs)
        return inner_func
    else:  # no options given
        def partial_inner(func):
            return replace_whitespace(func, **options)
        return partial_inner


# decorator  # https://www.fileformat.info/info/unicode/char/1f44f/index.htm
clapping_hands = replace_whitespace(replacement="\N{Clapping Hands Sign}")


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

    change_whitespace = replace_whitespace(func, r='\t' * 5)
    print(change_whitespace('my tabs are wide'))
