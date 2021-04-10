#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# is_same_as_prev.py

"""
is_same_as_prev is made to be called multiple times
is_same_as_prev saves the previous value and compares it with the current value
thus is_same_as_prev can detect changes in sequences

when is_same_as_prev is called for the first time it returns True
when is_same_as_prev is called again with the same value as parameter it returns True
when is_same_as_prev is called again with another value as parameter it returns False
when is_same_as_prev is called again with the same value as the previous time it returns True

after is_same_as_prev is called if has two attributes: current and previous
is_same_as_prev.current returns the latest given value
is_same_as_prev.previous returns the value before the latest given value

is_same_as_prev can also be used just to check the current with the previous
when keyword-only parameter: just_check is set to True the previous is kept as the previous
"""


def is_same_as_prev(current: object, *, just_check: bool = False) -> bool:
    """ check if the given current is the same as the previous received """
    self = is_same_as_prev  # set self for readability
    try:  # first time doesn't have previous so AttributeError is raised
        return bool(current == self.__prev)
    except AttributeError:
        self.__prev = current  # set current as previous array
        return is_same_as_prev(current)  # first call is always True
    finally:  # always set the attributes
        self.previous = self.__prev  # set is_same_as_prev.previous
        self.current = current  # set is_same_as_prev.current
        # keep the previous if just_check is set to True
        self.__prev = current if not bool(just_check) else self.__prev


if __name__ == '__main__':
    print("the function is not called and thus has no attributes")
    try:
        is_same_as_prev.previous
    except AttributeError:
        print("is_same_as_prev.previous doesn't yet exist")

    try:
        is_same_as_prev.current
    except AttributeError:
        print("is_same_as_prev.current doesn't yet exist")

    print("call is_same_as_prev and print the attributes and the result")
    first: bool = is_same_as_prev(True)
    assert first == True, "the first call of is_same_as_prev is always True"
    print(f"previous: {is_same_as_prev.previous}, current: {is_same_as_prev.current} -> {first}")
    second: bool = is_same_as_prev(False)
    print(f"previous: {is_same_as_prev.previous}, current: {is_same_as_prev.current} -> {second}")
    third: bool = is_same_as_prev(False)
    print(f"previous: {is_same_as_prev.previous}, current: {is_same_as_prev.current} -> {third}")
    print("keep the previous a.k.a. just check")
    four: bool = is_same_as_prev(..., just_check=True)
    print(f"previous: {is_same_as_prev.previous}, current: {is_same_as_prev.current} -> {four}")
    four: bool = is_same_as_prev(None, just_check=True)
    print(f"previous: {is_same_as_prev.previous}, current: {is_same_as_prev.current} -> {four}")

    print("endless loop:")
    import time
    from itertools import cycle
    for cur in cycle([1, 1, 2, 2, 3]):
        result = is_same_as_prev(cur)
        print(f"current: {cur} is same as prev.: {result}", end="\n" if result else " ")
        if not result:
            print(f"-> {is_same_as_prev.previous} == {is_same_as_prev.current}")
        time.sleep(1)
