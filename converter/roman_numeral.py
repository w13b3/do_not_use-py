#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# roman_numeral.py

# currently this script can represent numbers from 1 to 3999

# todo: add vinculum-notation
# todo: add single use numerals (subtractive) in and outside the vinculum-notation

# int: str
_number_to_numerals = {
    1: 'I',      # 'Ⅰ' \N{Roman Numeral One}
    2: 'II',     # 'Ⅱ' \N{Roman Numeral Two}
    3: 'III',    # 'Ⅲ' \N{Roman Numeral Three}
    4: 'IV',     # 'Ⅳ' \N{Roman Numeral Four}
    5: 'V',      # 'Ⅴ' \N{Roman Numeral Five}
    6: 'VI',     # 'Ⅵ' \N{Roman Numeral Six}
    7: 'VII',    # 'Ⅶ' \N{Roman Numeral Seven}
    8: 'VIII',   # 'Ⅷ' \N{Roman Numeral Eight}
    9: 'IX',     # 'Ⅸ' \N{Roman Numeral Nine}
    10: 'X',     # 'Ⅹ' \N{Roman Numeral Ten}
    # 11: 'XI',  # 'Ⅺ' \N{Roman Numeral Eleven}
    # 12: 'XII', # 'Ⅻ' \N{Roman Numeral Twelve}
    50: 'L',     # 'Ⅼ' \N{Roman Numeral Fifty}"
    90: 'XC',
    100: 'C',    # 'Ⅽ' \N{Roman Numeral One Hundred}
    400: 'CD',
    500: 'D',    # 'Ⅾ' \N{Roman Numeral Five Hundred}
    900: 'CM',
    1000: 'M'    # 'Ⅿ' \N{Roman Numeral One Thousand}
}
# sort numbers large -> small
number_to_numerals = dict(sorted(_number_to_numerals.items(), reverse=True))
# flip the dictionary key <-> value
numerals_to_number = {v.strip(): k for k, v in number_to_numerals.items()}


def convert_to_roman(number: int) -> str:
    """
    Convert a given number to (uppercase) roman numerals
    :param number: number to convert
    :type number: int
    :return: roman numerals
    :rtype: str
    """
    # define an empty string to concat the numerals onto
    numerals = ""
    # loop over the key: value pair in the number_to_numerals dictionary
    for numeral_value, letter in number_to_numerals.items():
        # concat the current numeral
        times = int(number // numeral_value)
        numerals += str(letter * times)
        # get the remainder of the division
        number = int(number % numeral_value)
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
    # clean given numerals
    numerals = roman_numerals.strip().upper()
    # make sure the given numerals are Roman numerals
    if not all(c in numerals_to_number.keys() for c in numerals):
        raise ValueError(f"given Roman numerals has non-roman numerals, given: {roman_numerals}")
    # define a starting number, in this case: zero
    number = 0
    # loop over the key: value pair in the numerals_to_number dictionary
    for letter, numeral_value in numerals_to_number.items():
        # count the amount of current letters in the given numerals
        times = numerals.count(letter)
        if times == 0:
            continue  # next in loop if no current letters are in the numerals
        # remove the letters that are counted
        numerals = numerals.replace(letter, '', times)
        # add the value of the letters to the number
        number += int(numeral_value * times)
        if len(numerals) == 0:
            break
    return number  # -> int


if __name__ == '__main__':
    import datetime

    cur_time = datetime.datetime.now()

    # current date time
    print(cur_time.strftime("%Y-%m-%d %H:%M:%S"))

    ryear = convert_to_roman(cur_time.year)
    rmonth = convert_to_roman(cur_time.month)
    rday = convert_to_roman(cur_time.day)
    rhour = convert_to_roman(cur_time.hour)
    rminute = convert_to_roman(cur_time.minute)
    rsecond = convert_to_roman(cur_time.second)

    # current date time in Roman numerals
    print(f"{ryear}-{rmonth}-{rday} {rhour}:{rminute}:{rsecond}")

    dyear = convert_to_number(ryear)
    dmonth = convert_to_number(rmonth)
    dday = convert_to_number(rday)
    dhour = convert_to_number(rhour)
    dminute = convert_to_number(rminute)
    dsecond = convert_to_number(rsecond)

    # current date time converted from Roman numerals (no leading 0)
    print(f"{dyear}-{dmonth}-{dday} {dhour}:{dminute}:{dsecond}")
