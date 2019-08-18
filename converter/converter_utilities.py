#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# converter_utilities.py

import keyword
import unicodedata


def is_valid_name(name: str) -> bool:
    """
    check if the variable name is valid
    use when str.isidentifier() can't be trusted
    """
    name = str(name).strip()  # condition the given name
    if not len(name) >= 1:  # assure the name given is longer than 0
        ValueError("expected name to be of lenght >= 1, %s" % len(name))
    if not _is_id_start(name[0]):  # take 1st char
        return False
    if len(name) > 1:  # if the length given of the name is longer than one
        for character in name[1:]:  # loop over characters
            if not _is_id_continue(character):  # check if continue chars are valid
                return False
    return True  # All characters are allowed.


def _is_id_start(character: str) -> bool:
    """ check if the character given is valid to start a variable name with """
    _allowed_id_start_categories = {"Ll", "Lm", "Lo", "Lt", "Lu", "Nl"}
    _allowed_id_start_characters = {"_", "\u2118", "\u212E", "\u309B", "\u309C"}
    if 0 < len(character) < 2:
        ValueError("Expected character to be lenght of 1, given: %d" % len(character))

    a = unicodedata.category(unicodedata.normalize("NFKC", character)) in _allowed_id_start_categories
    b = unicodedata.normalize("NFKC", character) in _allowed_id_start_characters
    c = unicodedata.category(character) in _allowed_id_start_categories
    d = character in _allowed_id_start_categories
    return any([a, b, c, d])  # -> bool


def _is_id_continue(character: str) -> bool:
    """ check if the character given is valid as characters in a variable name """
    _allowed_id_continue_categories = {"Ll", "Lm", "Lo", "Lt", "Lu", "Mc", "Mn", "Nd", "Nl", "Pc"}
    _allowed_id_continue_characters = {"_", "\u00B7", "\u0387", "\u1369", "\u136A",
                                            "\u136B", "\u136D", "\u136E", "\u136C",
                                            "\u136F", "\u1370", "\u1371", "\u19DA",
                                            "\u2118", "\u212E", "\u309B", "\u309C"}
    if 0 < len(character) < 2:
        ValueError("Expected character to be lenght of 1, given: %d" % len(character))

    a = unicodedata.category(unicodedata.normalize("NFKC", character)) in _allowed_id_continue_categories
    b = unicodedata.normalize("NFKC", character) in _allowed_id_continue_characters
    c = unicodedata.category(character) in _allowed_id_continue_categories
    d = character in _allowed_id_continue_characters
    return any([a, b, c, d])  # -> bool


def condition_identifier(identifier,
                         leading_digit_char: str = 'd',
                         space_replace_char: str = '_',
                         invalid_replace_char: str = '_',
                         **kwargs) -> str:

    # # contracts
    # space_replace_char
    if _is_id_continue(space_replace_char):
        ValueError("given space_replace_char is not valid to be used in a variable, %s" % str(space_replace_char))
    if 0 <= len(space_replace_char) < 2:
        ValueError("expected space_replace_char to be of length 1 or 0, %s" % len(space_replace_char))
    # leading_digit_char
    if _is_id_start(leading_digit_char):
        ValueError("given leading_digit_char is not valid to start a variable with, %s" % str(leading_digit_char))
    if leading_digit_char.startswith("_"):  # namedtuple can't handle `_` 'coz it is reserved for functions
        ValueError("given leading_digit_char may not be used, %s" % str(leading_digit_char))
    # invalid_replace_char
    if _is_id_start(invalid_replace_char):
        ValueError("given invalid_replace_char is not valid to start a variable with, %s" % str(invalid_replace_char))
    if _is_id_continue(invalid_replace_char):
        ValueError("given invalid_replace_char is not valid to be used in a variable, %s" % str(invalid_replace_char))

    # if tuple, check if there is a string in the tuple
    # otherwise get the 1st value in the tuple
    if type(identifier) is tuple:
        for item in identifier:
            if isinstance(item, str):
                identifier = str(item)
                break
        else:
            identifier = str(identifier[0])

    # identifier names must be strings
    # condition keyword, strip the leading underscores
    identifier = str(identifier).strip().lstrip("_")

    # identifier may not be a keyword
    if keyword.iskeyword(identifier):
        identifier = identifier + "_"
        return identifier

    if len(identifier) == 1 and not _is_id_start(identifier) and not identifier.isdigit():
        identifier = str(ord(identifier))  # '$' -> 36
    if identifier.isdigit() or (not _is_id_start(identifier[0]) and identifier[0].isdigit()):
        identifier = str(leading_digit_char) + identifier  # add a letter in front of the digit

    # identifiers cannot have spaces between names
    identifier = identifier.replace(" ", str(space_replace_char))

    if not identifier.isidentifier():
        if not _is_id_start(identifier[0]):
            identifier = str(invalid_replace_char) + identifier[1:]

        _identifier = ""  # empty string to append to
        for char in identifier:
            if not _is_id_continue(char):
                char = str(invalid_replace_char)
            _identifier += char
        identifier = _identifier

        if all([letter == '_' for letter in identifier]):
            identifier = 'underscore' + '_' * len(identifier)
        else:
            # identifier names cannot start with an underscore
            identifier = identifier.lstrip("_")

        if not identifier.isidentifier():  # if the identifier is still not valid, run it again
            condition_identifier(identifier, leading_digit_char, space_replace_char, invalid_replace_char, **kwargs)

    return identifier  # -> str

if __name__ == '__main__':
    print(condition_identifier("$"))
