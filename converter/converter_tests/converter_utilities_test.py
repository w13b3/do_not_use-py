#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# converter_utilities_test.py

import keyword
import unittest
from converter import converter_utilities


class ConverterUtilitiesTest(unittest.TestCase):

    def test_is_valid_name(self):
        is_valid_name = converter_utilities.is_valid_name
        valid_names = ["__hidden", "_not_puplic", "public", "Q1", "a2", "_123ABC"]
        invalid_names = [1, "2", "$", "%_", "!", 1_000_000, "1234567890!@#$%^&*()+-=", b"byte"]

        for name in valid_names:
            result = is_valid_name(name)
            self.assertTrue(result, msg=name)

        for name in invalid_names:
            result = is_valid_name(name)
            self.assertFalse(result, msg=name)


    def test_is_id_start(self):
        is_id_start = converter_utilities._is_id_start
        valid_start_chars = ("_", "a", "A", "き", "キ", "中", "ஹ")
        invalid_start_chars = ("█", "█", "█", "▒", "▒", "░", "█", "█", "▒")

        for char in valid_start_chars:
            char = str(char).strip()  # hidden functions should not condition values
            result = is_id_start(char)
            self.assertTrue(result)

        for char in invalid_start_chars:
            char = str(char).strip()  # hidden functions should not condition values
            result = is_id_start(char)
            self.assertFalse(result)

    def test_is_id_continue(self):
        is_id_continue = converter_utilities._is_id_continue
        valid_continue_chars = ("_", "a", "A", "き", "キ", "中", "5")  # <- difference over test_is_id_start
        invalid_continue_chars = ("█", "█", "█", "▒", "▒", "░", "█", "█", "▒")

        for char in valid_continue_chars:
            char = str(char).strip()  # hidden functions should not condition values
            result = is_id_continue(char)
            self.assertTrue(result)

        for char in invalid_continue_chars:
            char = str(char).strip()  # hidden functions should not condition values
            result = is_id_continue(char)
            self.assertFalse(result)

    def test_condition_identifier(self):
        condition_identifier = converter_utilities.condition_identifier
        names = ["__hidden", "_not_puplic", "public", "Q1", "a2", "_123ABC", "class", "space in name"]
        expected_names = ["hidden", "not_puplic", "public", "Q1", "a2", "d123ABC", "class_", "space_in_name"]
        invalid_names = [1, "2", "$", "%_", "!", 1_000_000, "1234567890!@#$%^&*()+-=", b"byte"]
        expected_invalid_names = ["d1", "d2", "d36", "underscore__", "d33",
                                  "d1000000", "d1234567890_____________", "b_byte_"]

        for name, expected in zip(names, expected_names):
            result = condition_identifier(name)
            self.assertTrue(bool(result))  # make sure something is returned
            self.assertEqual(expected, result)

        for name, expected in zip(invalid_names, expected_invalid_names):
            result = condition_identifier(name)
            self.assertTrue(bool(result))  # make sure something is returned
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
