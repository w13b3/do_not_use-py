#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# roman_numerals.py

# Dict[int, str]
_number_to_numerals = {
    1: 'I',        # 'Ⅰ' \N{Roman Numeral One}
    # 2: 'II',     # 'Ⅱ' \N{Roman Numeral Two}
    # 3: 'III',    # 'Ⅲ' \N{Roman Numeral Three}
    4: 'IV',       # 'Ⅳ' \N{Roman Numeral Four}
    5: 'V',        # 'Ⅴ' \N{Roman Numeral Five}
    # 6: 'VI',     # 'Ⅵ' \N{Roman Numeral Six}
    # 7: 'VII',    # 'Ⅶ' \N{Roman Numeral Seven}
    # 8: 'VIII',   # 'Ⅷ' \N{Roman Numeral Eight}
    9: 'IX',       # 'Ⅸ' \N{Roman Numeral Nine}
    10: 'X',       # 'Ⅹ' \N{Roman Numeral Ten}
    # 11: 'XI',    # 'Ⅺ' \N{Roman Numeral Eleven}
    # 12: 'XII',   # 'Ⅻ' \N{Roman Numeral Twelve}
    40: 'XL',
    50: 'L',       # 'Ⅼ' \N{Roman Numeral Fifty}"
    90: 'XC',
    100: 'C',      # 'Ⅽ' \N{Roman Numeral One Hundred}
    400: 'CD',
    500: 'D',      # 'Ⅾ' \N{Roman Numeral Five Hundred}
    900: 'CM',
    1000: 'M'      # 'Ⅿ' \N{Roman Numeral One Thousand}
}

# sort numbers large -> small
number_to_numerals = dict(sorted(_number_to_numerals.items(), reverse=True))


def convert_to_numeral(number: int) -> str:
    """
    Convert a given number to (uppercase) Roman numerals
    :param number: number to convert
    :type number: int
    :return: Roman numerals
    :rtype: str
    """
    # assure given number is of type int
    if not isinstance(number, int):
        raise ValueError("expected number to be of type: int")
    if number <= 0:  # no zero or negative
        raise ValueError("negative numbers or zero is not available as Roman numeral")
    if number > 3999999:  # vinculum-notation limit
        raise ValueError("given number is above the available Roman numeral range")

    # define empty numerals string
    numerals = ""
    if int(number) > 3999:  # Standard Roman numeral limit
        v_number = int(number // 1000)
        # leftover number reused in the for-loop
        number = int(number % 1000)
        # use the integer division outcome as number
        v_notation: str = convert_to_numeral(v_number)  # recursive
        numerals += f"({v_notation})"  # bracket vinculum-notation

    # loop over the key: value pair in the number_to_numerals dictionary
    for value, numeral in number_to_numerals.items():
        # if the number is less than the numeral_value; go check the next numeral_value
        if number < value:
            continue  # next loop
        # define how much times the current numeral, should never be more than 3
        times = int(number // value)
        # concat the current numeral
        numerals += str(numeral * times)
        # get the remainder of the division
        number = int(number % value)  # -1 % 1000 = 999
        # if the remainder is 0, stop the loop
        if number == 0:
            # Roman numerals has no zero
            break

    return numerals  # -> str


def convert_to_number(roman_numerals: str) -> int:
    """
    Convert Roman numerals to a number
    Roman numerals are written from left to right,
      and from highest to lowest (in terms of individual numeral value)
    :param roman_numerals: Roman numeral to convert
    :type roman_numerals: str
    :return: number
    :rtype: int
    """
    # assure the given Roman numerals is of type: str
    if not isinstance(roman_numerals, str):
        raise ValueError("expected given numerals to be of type: str")

    # define a starting number, in this case: zero
    number: int = 0
    # clean and make given numerals uppercase
    numerals: str = roman_numerals.strip().upper()

    brackets = ('(', ')')
    if any(c for c in numerals if c in brackets):
        # Numerals bracket vinculum-notation should start with bracket open
        if not numerals.startswith('('):
            raise ValueError("Roman numerals with bracket vinculum-notation should start with '('")
        # Numerals bracket vinculum-notation should have only one opening and one closing bracket
        for c in brackets:
            if numerals.count(c) > 1:
                raise ValueError(f"numerals can only have one '{c}'")
        # split the Numeral with bracket vinculum-notation
        # (MMMCMXCIX)CMXCIX -> 'MMMCMXCIX', _, 'CMXCIX'
        v_notation, _, numerals = numerals[1:].partition(")")
        number = int(convert_to_number(v_notation) * 1000)

    # make sure the given numerals are Roman numerals
    if not all(c in number_to_numerals.values() for c in numerals):
        raise ValueError("given Roman numerals contains non-roman numerals")

    # loop over the key: value pair in the numerals_to_number dictionary
    for value, numeral in number_to_numerals.items():
        count = 0  # could replace while loop with count from itertools
        while numerals.startswith(numeral):
            # 'pop' the first numeral and keep the leftover numerals
            numerals = numerals[len(numeral):]
            count += 1
            # Numerals can't have 3 of the same numeral in a row
            if count > 3:
                raise ValueError("Roman numerals can't have 3 of the same numeral in a row")
        # add the value of the letters to the number
        number += int(value * count)

        # if there is no more numerals, stop the loop
        if not numerals:
            break

    # Roman numerals are written from high to low value (M -> I)
    if numerals:
        raise ValueError("given numerals are not in valid order")

    return number  # -> int


if __name__ == '__main__':
    "local test"
    for _value, _numeral in number_to_numerals.items():
        to_number = convert_to_number(_numeral)
        assert _value == to_number, f"convert_to_number, expected: {_value} received: {to_number} "

        to_numeral = convert_to_numeral(_value)
        assert _numeral == to_numeral, f"convert_to_numeral, expected: {_value} received: {to_numeral} "

    _numbers = [3999, 4000, 444444, 999999, 3999999]
    _numerals = ["MMMCMXCIX", "(IV)", "(CDXLIV)CDXLIV", "(CMXCIX)CMXCIX", "(MMMCMXCIX)CMXCIX"]

    for _number, _numeral in zip(_numbers, _numerals):
        to_number = convert_to_number(_numeral)
        assert _number == to_number, f"convert_to_number, expected: {_number} received: {to_number} "
        to_numeral = convert_to_numeral(_number)
        assert _numeral == to_numeral, f"convert_to_numeral, expected: {_numeral} received: {to_numeral} "

    for _n in [-1, 0, 4000000]:
        try:
            convert_to_numeral(_n)
        except ValueError as err:
            print(f"{_n}: {err}")
            pass

    for _c in ["-I", "Y", 0, "(I))", "((I)", "I(V)", "VVVV", "XLXLXLXL", "XLL"]:
        try:
            convert_to_number(_c)
        except ValueError as err:
            print(f"{_c}: {err}")
            pass
