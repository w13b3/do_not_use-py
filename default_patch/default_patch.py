#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# default_patch.py

import inspect
import functools
import itertools

# known feature(s):
# >>> func = lambda x: print(x)
# >>> func = default_patch(func, x=False)
# >>> func(True, x=True)  # 'SyntaxError: keyword argument repeated' expected here
# True
# # #
# >>> class C:
# >>>     def func(self, x, y=None): return x, y
# >>>     func = default_patch(func, y=True)
# >>>     func('x')  # error here
# >>> C()
# TypeError: func() missing 1 required positional argument: 'x'


def default_patch(func: callable = None, **options) -> callable:
    """
    :param func: function to give the default values to
    :type func: callable
    :param options: default keyword arguments that are related to the given function
    :return: the function that is given
    :rtype: callable

    example usage:
    >>> func1 = lambda x: print(x)
    >>> func1 = default_patch(func1, x='hello')
    >>> func1()
    hello
    >>> def function2(a, b={1: 'One'}):
    ...     return a, b
    ...
    >>> func2 = default_patch(function2, a=False, b={2: 'Two'})
    >>> func2(True)
    (True, {2: 'Two'})
    >>> func2(True, b={3: 'Three'})
    (True, {2: 'Two', 3: 'Three'})
    """

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
    def _(func_value, default_value):
        new_value = {**default_value, **func_value}  # overwrite keyword-value of default
        return new_value

    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        parameter_names = tuple(func_info.args + func_info.kwonlyargs)

        # check if wrapped in
        in_class = False
        if len(args) > 0:
            in_class = hasattr(args[0], func.__name__)  # self has attribute of function name
        if bool(in_class):
            _, *parameter_names = parameter_names  # remove 'self'
            self, *args = args  # args become a list

        args_to_kwargs = {key: value for value, key in zip(args, parameter_names)}
        all_kwargs = {**kwargs, **args_to_kwargs}  # given arguments have priority

        # extend singledispatch types
        for item_key, item_value in all_kwargs.items():
            if item_key not in options:
                continue
            option_val = options.get(item_key, None)
            if not type(option_val) == type(item_value):
                continue
            new_value = extend_value(item_value, option_val)
            all_kwargs[item_key] = new_value

        final_kwargs = {**options, **all_kwargs}
        return func(self, **final_kwargs) if in_class else func(**final_kwargs)  # return the function

    # given func should be a callable
    if func is not None and not callable(func):
        raise ValueError(f'Expected func to be a callable, got: {type(func)!r}')

    if not bool(options):  # no options are given
        return func  # do nothing

    if callable(func):  # decorator   with   options.
        func_info = inspect.getfullargspec(func)
        if not bool(func_info.varkw):  # if there is no **keywords available in the function
            given, available_options = set(options.keys()), set(func_info.args + func_info.kwonlyargs)
            if not given.issubset(available_options):  # check if wrong keywords are given
                diff = given.difference(available_options)
                raise ValueError(
                    f'Given callable: {func.__name__!r} does not accept the following keyword(s): {diff!r}')

        return inner_func
    else:
        def partial_inner(func):  # decorator   without   options.
            return default_patch(func, **options)
        return partial_inner
