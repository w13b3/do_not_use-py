#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# is_equal_as_previous.py

"""
is_equal_as_previous is made to be called multiple times
is_equal_as_previous saves the previous value and compares it with the current value
thus is_equal_as_previous can detect changes in sequences

when is_equal_as_previous is called for the first time it returns True
when is_equal_as_previous is called again with the same value as parameter it returns True
when is_equal_as_previous is called again with another value as parameter it returns False
when is_equal_as_previous is called again with the same value as the previous time it returns True

after is_equal_as_previous is called if has two attributes: current and previous
is_equal_as_previous.current returns the latest given value
is_equal_as_previous.previous returns the value before the latest given value

is_same_as_prev can also be used just to check the current with the previous
when keyword-only parameter: just_check is set to True the previous is kept as the previous
"""


# avg. of 1_000_000: 0.322166
def is_equal_as_previous1(current: object, *, just_check: bool = False) -> bool:
    """ check if the given current is the same as the previous received """
    self = is_equal_as_previous1  # set self for readability
    try:  # first time doesn't have previous so AttributeError is raised
        return bool(current == self.__memory)
    except AttributeError:
        self.__memory = current  # set current as previous array
        return self(current)  # first call is always True
    finally:  # always set the attributes
        self.previous = self.__memory  # set is_same_as_prev.previous
        self.current = current  # set is_same_as_prev.current
        if not bool(just_check):  # keep the previous if just_check is set to True
            self.__memory = current


# monkey patch
is_equal_as_previous = is_equal_as_previous1


# avg. of 1_000_000: 0.342118
def is_equal_as_previous2(current: object, *, just_check: bool = False) -> bool:
    """ check if the given current value is the same as the previous received value """
    self = is_equal_as_previous2
    __memory = current  # set memory as current to prevent UnboundLocalError
    try:
        __memory = self.prev_cur[1]  # take and assign the second of the list
        self.prev_cur = [__memory, current]  # create a new list
        return bool(__memory == current)  # equality test
    except AttributeError:
        self.prev_cur = [current, current]  # fill the prev_cur list
        self.previous = self.current = current  # first call set attributes
        return self(current)   # first call is always True
    finally:
        if not bool(just_check): # keep the previous if just_check is set to True
            self.previous, self.current = __memory, current


# avg. of 1_000_000: 1.250343
def is_equal_as_previous3(current: object, *, just_check: bool = False) -> bool:
    """ check if the given current value is the same as the previous received value """
    self = is_equal_as_previous3  # self refers to this function

    def get_previous() -> object:
        """ get the memory attribute that represents the previous value """
        if not hasattr(self, '__memory'):
            set_previous(current)  # take current from main func. and set it as memory
        return self.__memory

    def set_previous(replacement: object):
        """ set a memory attribute that represents the previous value """
        self.__memory = replacement

    def equal_as_previous(current_value: object, *, only_check: bool = False) -> bool:
        """ test the given value against the previously given value """
        previous_value = get_previous()
        _equality_test = bool(previous_value == current_value)
        # only checking doesn't set previous or re-assign the attributes
        if not bool(only_check):
            set_previous(current_value)
            self.previous, self.current = previous_value, current_value
        # assure that even the first call has the attributes
        if any(not hasattr(self, _) for _ in ('previous', 'current')):
            self.previous, self.current = previous_value, current_value
        return _equality_test  # -> bool

    return equal_as_previous(current, only_check=just_check)


if __name__ == '__main__':
    eq = is_equal_as_previous1
    # eq = is_equal_as_previous2
    # eq = is_equal_as_previous3

    print("the function is not called and thus has no attributes")
    try:
        eq.previous
    except AttributeError:
        print("is_same_as_prev.previous doesn't yet exist")

    try:
        eq.current
    except AttributeError:
        print("is_same_as_prev.current doesn't yet exist")

    print("call is_same_as_prev and print the attributes and the result")
    first: bool = eq(True)
    assert first == True, "the first call of is_same_as_prev is always True"
    print(f"previous: {eq.previous}, current: {eq.current} -> {first}")
    second: bool = eq(False)
    print(f"previous: {eq.previous}, current: {eq.current} -> {second}")
    third: bool = eq(False)
    print(f"previous: {eq.previous}, current: {eq.current} -> {third}")
    print("keep the previous a.k.a. just check")
    four: bool = eq(..., just_check=True)
    print(f"previous: {eq.previous}, current: {eq.current} -> {four}")
    five: bool = eq(None, just_check=True)
    print(f"previous: {eq.previous}, current: {eq.current} -> {five}")

    print("endless loop:")
    import time
    from itertools import cycle
    for cur in cycle([1, 1, 2, 2, 3]):
        result = eq(cur)
        print(f"current: {cur} is same as prev.: {eq.previous}", end="\n" if result else " ")
        if not result:
            print(f"-> {eq.previous} == {eq.current}")
        time.sleep(1)

    import timeit
    # setup = "from __main__ import is_equal_as_previous1, is_equal_as_previous2, is_equal_as_previous3"
    # print('is_equal_as_previous1', timeit.timeit("is_equal_as_previous1(None)", setup, number=1_000_000))
    # print('is_equal_as_previous2', timeit.timeit("is_equal_as_previous2(None)", setup, number=1_000_000))
    # print('is_equal_as_previous3', timeit.timeit("is_equal_as_previous3(None)", setup, number=1_000_000))
