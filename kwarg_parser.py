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
