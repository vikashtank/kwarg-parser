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

    def validate(self, kwargs):
        for validator in  self._validators:
            validator.validate(kwargs)

    def __call__(self, function):

        def validator(*args, **kwargs):
            self.validate(kwargs)
            return function(*args, **kwargs)

        return validator

class MutuallyExclusive(Validator):
    pass

    def __init__(self, *arg_names: str):
        self.arg_names = arg_names

    def validate(self, kwargs):

        arg_names = set(self.arg_names)
        kwarg_names = set(kwargs.keys())
        intersection = arg_names & kwarg_names

        if len(intersection) > 1:
            raise ValidationError(" mutually_exclusive arguments:"
                                  f" {intersection} cannot appear together")
