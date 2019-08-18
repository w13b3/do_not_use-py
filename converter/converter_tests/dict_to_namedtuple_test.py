#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# dict_to_namedtuple_test.py

import unittest
from collections import namedtuple
from converter.dict_to_namedtuple import to_namedtuple


class DictToNamedtuple(unittest.TestCase):

    def test_to_namedtuple_no_recursive(self):
        d = {"key_1": 1, "key_2": 2, "key_3": True}
        result = to_namedtuple(d)
        # namedtuple will contain a key_3 that returns True
        self.assertTrue(result.key_3)

    def test_to_namedtuple_recursive(self):
        d = {"key_1": 1, "key_2": 2, "key_3": {"key_4": True}}
        result = to_namedtuple(d, keep_dicts=False)
        # false keep_dicts means the nested dicts are converted to namedtuple too.
        # key_3 will be a namedtuple with key_4 returning True
        self.assertTrue(result.key_3.key_4)

    def test_to_namedtuple_dict_with_other_containers(self):
        d = {"_list": [1, 2, 3], "_set": {1, 2, 3}, "_tuple": (1, 2, 3), "_dict": {1: 1, 2: 2, 3: 3}}
        # due to conversion the leading underscores are stripped
        # _list --became--> list

        result = to_namedtuple(d, keep_dicts=True)
        self.assertIsInstance(result.list, list)
        self.assertIsInstance(result.set, set)
        self.assertIsInstance(result.tuple, tuple)
        self.assertIsInstance(result.dict, dict)  # keep_dicts = True

        result_recursive = to_namedtuple(d, keep_dicts=False)
        self.assertIsInstance(result_recursive.list, list)
        self.assertIsInstance(result_recursive.set, set)
        self.assertIsInstance(result_recursive.tuple, tuple)

    def test_to_namedtuple_errors(self):
        d = {"_underscore": 1, "__underscore": 1}
        # due to conversion the leading underscores are stripped
        # this results in not-unique keywords
        with self.assertRaises(ValueError):
            to_namedtuple(d)

        invalid_containers = (["a", "list"], ("tu", "ple"), {"set", "tes"})
        invalid_types = ("str", 1, 2.3, 4j)
        # only dict is accepted, others raise an ValueError
        with self.assertRaises(ValueError):
            for d in invalid_containers:
                to_namedtuple(d)
            for d in invalid_types:
                to_namedtuple(d)


if __name__ == '__main__':
    unittest.main()
