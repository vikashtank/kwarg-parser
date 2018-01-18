import os
this_directory = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.append(this_directory + "/../")
import kwarg_parser as kp
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.parser = kp.Parser()
        mutually_exclusive = kp.MutuallyExclusive("arg1", "arg2", "arg3")
        self.parser.add_validator(mutually_exclusive)

    def test_mutually_exclusive_pass(self):

        @self.parser
        def example_1(**kwargs):
            pass

        example_1(arg1 = "hey")

    def test_mutually_exclusive_fail(self):

        @self.parser
        def example_1(**kwargs):
            pass

        with self.assertRaises(kp.ValidationError):
            example_1(arg1 = "hey", arg2 = "no")


class TestMutuallyExclusive(unittest.TestCase):

    def setUp(self):
        self.mutually_exclusive = kp.MutuallyExclusive("hello", "bye", "hey")


    def test_validate(self):
        self.mutually_exclusive.validate({"hello": 1, "boy": 2, "hay": 3})

    def test_validate_zero(self):
        self.mutually_exclusive.validate({"helelo": 1, "boy": 2, "hay": 3})

    def test_validate_failure(self):
        with self.assertRaises(kp.ValidationError):
            self.mutually_exclusive.validate({"hello": 1, "bye": 2, "hay": 3})





if __name__ == "__main__":
    unittest.main()
