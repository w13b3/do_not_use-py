#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# deco.py

import functools


def assure(func: callable = None, **options) -> callable:
    """
    wrapper for a function which parameter should be exact as expected
    the given option should be exactly named as the parameter of the wrapped function
    """
    if func is not None:
        @functools.wraps(func)
        def inner_func(*___wrap_args, **___wrap_kwargs):
            # create kwargs from given arguments and keyword-arguments and its values
            func_kw = {**dict(zip(func.__code__.co_varnames, ___wrap_args)), **___wrap_kwargs}
            assert not any(_ in ___wrap[:2] for _ in func_kw), err_msg
            for opt_key, opt_val in options.items():
                try:  # check if the given option's value is the same as the function-value
                    kw = func_kw[opt_key]
                    if isinstance(opt_val, tuple):
                        if kw not in opt_val:
                            return  # -> None
                    elif kw != opt_val:
                        return  # -> None
                except KeyError:  # option not in the func-params
                    continue
            else:  # no break and no return in the for-loop
                return func(*___wrap_args, **___wrap_kwargs)   # -> callable ( execute the function )

        err_msg = "decorator 'assure' is double stacked or wrapped twice"
        ___wrap = inner_func.__code__.co_varnames
        return inner_func
    else:  # no options given
        def partial_inner(func):
            return assure(func, **options)
        return partial_inner


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

    # assure decorator

    @assure(b=(2, 3))
    def f(a, b):
        return a, b

    print(f(1, 2))
    print(f(2, 3))
    print(f(3, 4))  # None, because 4 is not in given assure decorator

    # AssertionError: decorator 'assure' is double stacked or wrapped twice
    # assure(f, b=4)(4, 4)
