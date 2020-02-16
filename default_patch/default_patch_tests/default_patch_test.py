#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# default_patch_test.py

import unittest

# from default_patch.default_patch import default_patch


class DefaultPatchTest(unittest.TestCase):

    def def_func(self, x): return x
    def_func = default_patch(def_func, x=True)

    def def_func_with_kwargs(self, x, **kwargs): return x
    def_func_with_kwargs = default_patch(def_func_with_kwargs, x=True)

    def def_func_with_default_arg(self, x, y=False): return x, y
    def_func_with_default_arg = default_patch(def_func_with_default_arg, y=True)

    def test_positional_arg_named_self(self):
        result = self.def_func()
        self.assertTrue(result)

    def test_bug_not_raising_invalid_syntax_when_positional_arg_and_keyword_of_same_parameter_is_given(self):
        result = self.def_func_with_default_arg(True, x=True)  # pos arg 'x' and keyword arg 'x' are both given here
        self.assertTrue(all(result))

        res_x, res_y = self.def_func_with_default_arg(False, x=True, y=False)  # pos args has priority over keyword arg
        self.assertFalse(res_x)
        self.assertFalse(res_y)  # both x and y returns false, thus x=True was not used; *arg has priority over **kwarg

    def test_given_function_should_be_callable_old(self):
        with self.assertRaises(ValueError):
            func = default_patch('local_func', x=True)  # str 'func' is not a callable

    def test_other_than_func_no_arguments_allowed(self):
        def local_def_func(x): return x

        with self.assertRaises(TypeError):
            func = default_patch(local_def_func, True)  # extra (not allowed) positional argument is given

    def test_should_raise_error_if_keywords_are_given_that_are_not_expected(self):
        # 2: should raise error if keywords are given that are not expected
        def local_def_func_no_kwargs(x): return x  # notice NO **kwargs
        def def_func_with_kwargs(x, **kwargs): return x  # notice the **kwargs

        with self.assertRaises(ValueError):
            func = default_patch(local_def_func_no_kwargs, z=True)  # kwarg 'z' is not defined in function without kwargs

        local_def_func_with_kwargs = default_patch(def_func_with_kwargs, x=True, z=True)  # multiple kwargs allowed
        result = local_def_func_with_kwargs()  # x is given as default above this line
        self.assertTrue(result)  # no error due to given function has the **kwargs

    def test_a_given_keyword_argument_must_be_prioritized_over_the_default_keyword_counterpart(self):
        result = self.def_func(x=False)  # given keyword overwrite the given default
        self.assertFalse(result)  # x=false -> result False

        result = self.def_func(x=True)  # give keyword
        self.assertTrue(result)  # given keyword and default keyword can be the same

        result = self.def_func(True)  # overwrite set default with positional argument
        self.assertTrue(result)

        # 'feature' ¯\_(ツ)_/¯
        # position argument and keyword argument for the same parameters
        result = self.def_func(True, x=False)  # normally this gives SyntaxError
        self.assertTrue(result)  # positional argument has priority over the keyword argument of the same parameter

    def test_default_kwargs_should_not_affect_the_given_func_kwargs(self):
        result = self.def_func()
        self.assertTrue(result)
        result = self.def_func('')  # False value
        self.assertFalse(result)
        result = self.def_func(x='')  # False value
        self.assertFalse(result)

    def test_given_set_must_be_extended_with_the_given_default_set(self):
        def local_func(x=None): return x

        set_value = {'a', 'value'}
        new_set_value = {'another', 'new_value'}
        extended_set_value = {'another', 'new_value', 'a', 'value'}

        set_func = default_patch(local_func, x=set_value)  # set default

        set_default_result = set_func()
        self.assertEqual(set_value, set_default_result)  # check default

        set_extended_result = set_func(new_set_value)
        self.assertEqual(extended_set_value, set_extended_result)  # check default extended
        self.assertIsInstance(set_extended_result, set)

    def test_given_list_must_be_extended_with_the_default_list(self):
        def local_func(x=None): return x

        list_value = ['a', 'value']
        new_list_value = ['another', 'new_value']
        extended_list_value = ['another', 'new_value', 'a', 'value']

        list_func = default_patch(local_func, x=list_value)  # set default

        list_default_result = list_func()
        self.assertEqual(list_value, list_default_result)  # check default
        self.assertListEqual(list_value, list_default_result)  # check default

        list_extended_result = list_func(new_list_value)
        self.assertEqual(extended_list_value, list_extended_result)  # check default extended
        self.assertListEqual(extended_list_value, list_extended_result)  # check default extended
        self.assertIsInstance(list_extended_result, list)

    def test_given_dict_must_be_extended_with_the_default_dict(self):
        def local_func(x=None): return x

        dict_value = {'a': 'value'}
        new_dict_value = {'another': 'new_value'}
        extended_dict_value = {'another': 'new_value', 'a': 'value'}

        dict_func = default_patch(local_func, x=dict_value)  # set default

        dict_default_result = dict_func()
        self.assertEqual(dict_value, dict_default_result)  # check default

        dict_extended_result = dict_func(new_dict_value)
        self.assertEqual(extended_dict_value, dict_extended_result)  # check default extended
        self.assertIsInstance(dict_extended_result, dict)

    def test_given_tuple_must_be_extended_with_the_default_tuple(self):
        def local_func(x=None): return x

        tuple_value = ('a', 'value')
        new_tuple_value = ('another', 'new_value')
        extended_tuple_value = ('another', 'new_value', 'a', 'value')

        tuple_func = default_patch(local_func, x=tuple_value)  # set default

        tuple_default_result = tuple_func()
        self.assertEqual(tuple_value, tuple_default_result)  # check default

        tuple_extended_result = tuple_func(new_tuple_value)
        self.assertEqual(extended_tuple_value, tuple_extended_result)  # check default extended
        self.assertIsInstance(tuple_extended_result, tuple)

    def test_default_type_should_be_the_same_as_given_type_otherwise_keep_given_skip_extending(self):
        def local_func(x=None): return x

        set_value = {'a', 'value'}
        list_value = ['a', 'value']
        dict_value = {'a': 'value'}
        tuple_value = ('a', 'value')

        set_func = default_patch(local_func, x=set_value)  # set default
        list_func = default_patch(local_func, x=list_value)
        dict_func = default_patch(local_func, x=dict_value)
        tuple_func = default_patch(local_func, x=tuple_value)

        other_type = 'string'
        set_result = set_func(other_type)  # give other type
        self.assertEqual(set_result, other_type)
        list_result = list_func(other_type)
        self.assertEqual(list_result, other_type)
        dict_result = dict_func(other_type)
        self.assertEqual(dict_result, other_type)
        tuple_result = tuple_func(other_type)
        self.assertEqual(tuple_result, other_type)  # check if other type is returned

    def test_overwrite_default_dict_keyword_with_given_dict(self):
        def local_func(x=None): return x

        dict_value = {'a': 'value'}
        expected_dict_value = new_dict_value = {'a': 'new_value'}  # set expected and new value
        len_expected_value = len(expected_dict_value)  # 1 item in dict == 1 lenght

        dict_func = default_patch(local_func, x=dict_value)  # set default

        dict_overwritten_result = dict_func(new_dict_value)
        self.assertEqual(expected_dict_value, dict_overwritten_result)  # check default is overwritten by given value
        self.assertEqual(len_expected_value, len(dict_overwritten_result))  # double check dict is not extended

    def test_general_usage(self):
        def local_func(x, y, z=None):
            # print(x, y, z)
            return x, y, z

        patched_function = default_patch(local_func, x=False, y=False)  # set default

        expected_result = (True, True, True)
        result = patched_function(True, True, True)
        self.assertEqual(result, expected_result)

        expected_result = (True, True, None)
        result = patched_function(True, True)
        self.assertEqual(result, expected_result)

        expected_result = (True, False, None)
        result = patched_function(True)
        self.assertEqual(result, expected_result)

        expected_result = (True, False, None)
        result = patched_function(True, x=True)
        self.assertEqual(result, expected_result)

        expected_result = (True, False, None)
        result = patched_function(True, x=False)
        self.assertEqual(result, expected_result)

        expected_result = (False, False, None)
        result = patched_function(False, x=True)  # 'feature' ¯\_(ツ)_/¯
        self.assertEqual(result, expected_result)

    def test_recursion(self):
        def local_func(x, y, z=None):
            # print(x, y, z)
            return x, y, z

        local_func = default_patch(local_func, x=True)  # set default
        local_func = default_patch(local_func, y=True)  # set default
        local_func = default_patch(local_func, z=True)  # set default
        recursive_function = local_func  # rename function

        expected_result = (True, True, True)
        result = recursive_function()  # no parameters, x y and z are set
        self.assertEqual(result, expected_result)

        expected_result = (True, True)
        def_func_with_default_arg = default_patch(self.def_func_with_default_arg, x=True)
        def_func_with_default_arg = default_patch(def_func_with_default_arg, y=True)  # overwrite func above
        result = def_func_with_default_arg()
        self.assertEqual(result, expected_result)

    def test_the_decorator_functionality(self):
        @default_patch  # no arguments
        def patched_no_kwarg(x, y, z=None): return x, y, z

        expected_result = (True, False, None)
        result = patched_no_kwarg(True, y=False)
        self.assertEqual(result, expected_result)

        @default_patch(y=True, z=True)  # with arguments
        def patched_func_with_kwargs(x, y, z=None): return x, y, z

        expected_result = (True, True, True)
        result = patched_func_with_kwargs(True)
        self.assertEqual(result, expected_result)

        expected_result = (False, True, False)
        result = patched_func_with_kwargs(False, z=False)  # overwrite default
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    print("start\n")

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("__main__").setLevel(logging.INFO)
    logging.captureWarnings(True)

    unittest.main()
