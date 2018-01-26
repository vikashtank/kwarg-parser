from abc import ABC, abstractmethod


class Validator(ABC):

    @abstractmethod
    def validate(self, kwargs):
        pass


class ValidationError(TypeError):
    pass


class Parser():

    def __init__(self):
        self._validators = []

    def add_validator(self, validator: Validator):
        self._validators.append(validator)

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, default_dict):
        self._default = default_dict

    def validate(self, kwargs):
        for validator in  self._validators:
            validator.validate(kwargs)

    def add_argument(self):
        pass

    def _try_apply_default(self, kwargs):
        """
        apply default values to inputs
        """
        try:
            for key, value in self.default.items():
                kwargs.setdefault(key, value)
        except AttributeError:
            pass

    def __call__(self, function):

        def validator(*args, **kwargs):
            self.validate(kwargs)
            self._try_apply_default(kwargs)
            return function(*args, **kwargs)

        return validator


class Argument(Validator):

    def __init__(self, name, default = None, type = None):
        self.name = name
        self.default = None
        self.type = type

    def validate(self, kwargs):
        value = self.validate_existance(kwargs)
        self.validate_type(value)

    def validate_existance(self, kwargs):
        try:
            return kwargs[self.name]
        except KeyError:
            raise ValidationError(f"argument: '{self.name}' does not exist")


    def validate_type(self, value):
        if not self._validate_type(value, self.type):
            raise ValidationError(f"'{value}' is not of type {self.type}")

    def _validate_type(self, value, type):
        return isinstance(value, int)



class MutuallyExclusive(Validator):


    def __init__(self, *arg_names: str):
        self.arg_names = arg_names

    def validate(self, kwargs):

        arg_names = set(self.arg_names)
        kwarg_names = set(kwargs.keys())
        intersection = arg_names & kwarg_names

        if len(intersection) > 1:
            raise ValidationError(" mutually_exclusive arguments:"
                                  f" {intersection} cannot appear together")

"""
TODO:

    add optional arguments
    add arguments to parser class
    add argument type specification
    add argument list size [*, +]
    add defaults to arguments
    errors for not specified arguments
    add groups" group = parser.add_argument_group(name)
                group.add_argument()
    add mutually_exclusive_group()
"""
