#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# default_patch.py

import inspect
import functools
import itertools
import contextlib

# known bug(s):
# >>> func = lambda x: print(x)
# >>> func = default_patch(func, x=False)
# >>> func(True, x=True)  # 'SyntaxError: keyword argument repeated' expected here
# True


def default_patch(func: callable, **default_kwargs) -> callable:
    """
    :param func: function to give the default values to
    :type func: callable
    :param default_kwargs: default keyword arguments that are related to the given function
    :return: the function that is given
    :rtype: callable

    example usage:
    >>> func1 = lambda x: print(x)
    >>> func1 = default_patch(function, x='hello')
    >>> func1()
    'hello'
    >>> def function2(a, b={1: 'One'}):
    ...     return a, b
    ...
    >>> func2 = default_patch(function2, a=False, b={2: 'Two'})
    >>> func2(True)
    True, {2: 'Two'}
    >>> func2(True, b={3: 'Three'})
    None, {2: 'Two', 3: 'Three'}
    """

    if not callable(func):
        raise ValueError(f'Expected func to be a callable, got: {type(func)!r}')

    func_info = inspect.getfullargspec(func)
    if not bool(func_info.varkw):  # if there is no **keywords available in the function
        given, available_options = set(default_kwargs.keys()), set(func_info.args + func_info.kwonlyargs)
        if not given.issubset(available_options):  # check if wrong keywords are given
            diff = given.difference(available_options)
            raise ValueError(f'Given callable: {func.__name__!r} does not accept the following keyword(s): {diff!r}')

    @functools.singledispatch
    def extend_value(func_value, default_value):
        return func_value  # not supported values gets returned as is

    @extend_value.register(set)
    @extend_value.register(list)
    @extend_value.register(tuple)
    def _(func_value, default_value):
        _builtins = __import__('builtins')  # get builtins object
        _type_name = type(func_value).__name__  # get name of type that was given
        # because set, list and tuple are builtin types this (hack) can be done
        new_value = getattr(_builtins, _type_name)(itertools.chain(func_value, default_value))  # insta-call
        return new_value

    @extend_value.register(dict)
    def _(func_value: dict, default_value: dict) -> dict:
        new_value = {**default_value, **func_value}  # overwrite keyword-value of default
        return new_value

    @functools.wraps(func)
    def inner_func(*func_args, **func_kwargs):
        # the following checks if self is given in the arguments
        #  if so: it removes it anc gives it uses it with the call of the function.
        self = False
        parameter_names = tuple(func_info.args + func_info.kwonlyargs)  # if given this includes self
        if bool(func_args):
            with contextlib.suppress(AttributeError):  # <arg> has no attribute <func.__name__>
                inspect.ismethod(getattr(func_args[0], func.__name__))  # check if 1st pos-arg is self
                # func_args (now a tuple) will become a list: https://twitter.com/raymondh/status/1205656939532734464
                self, *func_args = func_args  # -> list
                _, *parameter_names = parameter_names  # remove 'self' from parameter names
        # print(f'is self included in the parameters: {bool(self)}')

        # add the given 'positional arguments' (func_args) to the 'keyword arguments' (func_kwargs)
        func_kwargs = {**func_kwargs, **{kw: arg for arg, kw in zip(func_args, parameter_names)}}

        func_kwargs_copy = func_kwargs.copy()  # make a copy of the variable that is going to change
        for f_key, f_val in func_kwargs_copy.items():
            if f_key not in default_kwargs:  # when there is no f_key in the default_keys, continue iteration
                continue
            d_val = default_kwargs.get(f_key)
            if not type(d_val) == type(f_val):  # when values are not of the same type, continue iteration
                continue
            new_val = extend_value(f_val, d_val)  # dispatch based on type of f_val
            func_kwargs[f_key] = new_val  # update the func_kwargs with the extended value

        new_kwargs = {**default_kwargs, **func_kwargs}  # combine the kwargs with priority for func_kwargs

        # if self is a positional argument if default patch is used in a class
        #  thus object reference needs to be given with the function
        return func(self, **new_kwargs) if bool(self) else func(**new_kwargs)  # -> callable

    inner_func.func = func
    # inner_func.args = default_args  # no args allowed
    inner_func.keywords = default_kwargs
    return inner_func
