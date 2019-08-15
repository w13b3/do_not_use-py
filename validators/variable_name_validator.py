#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# variable_name_validator.py

"""
Python has keywords that may not be overwritten
also variable names may not start with numbers or contain special characters
this script is to validate the variable names or remove invalid characters of given names
"""


import keyword
import unicodedata

# Thanks Ghostkeeper ~ https://stackoverflow.com/a/41560708

_allowed_id_start_categories = {"Ll", "Lm", "Lo", "Lt", "Lu", "Nl"}
_allowed_id_start_characters = {"_", "\u2118", "\u212E", "\u309B", "\u309C"}
_allowed_id_continue_categories = {"Ll", "Lm", "Lo", "Lt", "Lu", "Mc", "Mn", "Nd", "Nl", "Pc"}
_allowed_id_continue_characters = {"_", "\u00B7", "\u0387", "\u1369", "\u136A", "\u136B", "\u136C", "\u136D", "\u136E",
                                        "\u136F", "\u1370", "\u1371", "\u19DA", "\u2118", "\u212E", "\u309B", "\u309C"}


def _is_id_start(character) -> bool:
    return unicodedata.category(character) in _allowed_id_start_categories \
           or character in _allowed_id_start_categories \
           or unicodedata.category(unicodedata.normalize("NFKC", character)) in _allowed_id_start_categories \
           or unicodedata.normalize("NFKC", character) in _allowed_id_start_characters


def _is_id_continue(character) -> bool:
    return unicodedata.category(character) in _allowed_id_continue_categories \
           or character in _allowed_id_continue_characters \
           or unicodedata.category(unicodedata.normalize("NFKC", character)) in _allowed_id_continue_categories \
           or unicodedata.normalize("NFKC", character) in _allowed_id_continue_characters


def is_valid_name(name: str) -> bool:
    """ check if the variable name is valid """
    if len(name) <= 0 or keyword.iskeyword(name):
        return False
    if not _is_id_start(name[0]):
        return False
    for character in name[1:]:
        if not _is_id_continue(character):
            return False
    return True  # All characters are allowed.


def remove_invalid_characters(name: str) -> str:
    """ remove all the characters that may not be used with variable names """
    if len(name) <= 0:
        raise ValueError("Given name should have a length of at least one")
    if keyword.iskeyword(name):
        raise ValueError("name should not be a keyword, given: %s" % name)

    num = 0
    for num, char in enumerate(name, num):
        if _is_id_start(char):
            break
    else:
        raise ValueError("Given name contained only invalid characters, given: %s" % name)

    return_name = ""
    for char in name[num:]:
        if _is_id_continue(char):
           return_name += char

    if len(return_name.strip()) == 0 and not is_valid_name(return_name):
        raise ValueError("How did you get here with: %s" % name)

    return return_name.strip()


if __name__ == '__main__':
    from copy import copy

    global_dict = copy(globals())

    for var_name in global_dict.keys():
        if not is_valid_name(var_name):
            # this would only trigger if python is broken
            raise SyntaxError("Variable name not valid")
