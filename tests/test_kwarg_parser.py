import os
this_directory = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(this_directory + "/../")
import kwarg_parser as kp
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.parser = kp.Parser()
        self.mutually_exclusive = kp.MutuallyExclusive("arg1", "arg2", "arg3")
        self.default = {"arg1": 0, "arg2": 2, "arg3": 5}

    def get_function(self):

        @self.parser
        def example(**kwargs):
            return kwargs

        return example

    def test_mutually_exclusive_pass(self):

        example = self.get_function()

        self.parser.add_validator(self.mutually_exclusive)
        example(arg1 = "hey")

    def test_mutually_exclusive_fail(self):

        example = self.get_function()

        self.parser.add_validator(self.mutually_exclusive)
        with self.assertRaises(kp.ValidationError):
            example(arg1 = "hey", arg2 = "no")

    def test_default(self):

        example = self.get_function()
        self.parser.default = self.default
        actual_dict = example(arg1 = "hey")
        expected_dict = {"arg1": "hey", "arg2": 2, "arg3":5}
        self.assertEqual(expected_dict, actual_dict)

    def test_non_existant_arg(self):

        example = self.get_function()

        self.parser.default = self.default
        actual_dict = example(arg7 = "hey")
        expected_dict = {"arg1": 0, "arg2": 2, "arg3":5, "arg7": "hey"}
        self.assertEqual(expected_dict, actual_dict)


class TestMutuallyExclusive(unittest.TestCase):

    def setUp(self):
        self.mutually_exclusive = kp.MutuallyExclusive("hello", "bye", "hey")

    def test_validate_single_match(self):
        self.mutually_exclusive.validate({"hello": 1, "boy": 2, "hay": 3})

    def test_validate_no_matches(self):
        self.mutually_exclusive.validate({"helelo": 1, "boy": 2, "hay": 3})

    def test_validate_failure_double_match(self):
        with self.assertRaises(kp.ValidationError):
            self.mutually_exclusive.validate({"hello": 1, "bye": 2, "hay": 3})

class TestArgument(unittest.TestCase):

    def setUp(self):
        self.argument = kp.Argument("hey")

    def test_validate(self):
        self.argument.type = int
        expected_dict = {"hey": 0, "arg2": 2}
        self.argument.validate(expected_dict)

    def test_validate_existance(self):
        self.argument.type = int
        expected_dict = {"hay": 0, "arg2": 2}
        with self.assertRaisesRegex(kp.ValidationError, "argument: 'hey' does not exist"):
            self.argument.validate(expected_dict)

    def test_validate_fail(self):
        self.argument.type = str
        expected_dict = {"hey": "str", "arg2": 2}
        with self.assertRaisesRegex(kp.ValidationError, "'str' is not of type <class 'str'>"):
            self.argument.validate(expected_dict)


if __name__ == "__main__":
    unittest.main()
