from .inputs.base import InputBase
from .inputs.bool import CheckboxInput
from .inputs.choice import RadioInput
from .inputs.choice import SelectInput
from .inputs.date import DateInput
from .inputs.date import DateTimeInput
from .inputs.date import TimeInput
from .inputs.file import FileInput
from .inputs.number import NumberInput
from .inputs.text import EMailInput
from .inputs.text import EMailInput
from .inputs.text import HiddenInput
from .inputs.text import PasswordInput
from .inputs.text import SearchInput
from .inputs.text import TextInput
from .inputs.text import UrlInput
from inspect import isclass


class InputProxy(object):
    def __getattr__(self, name):
        return getattr(self._input, name)

    def __init__(self, form, input):
        self._form = form
        self._input = input

    def _validate_item_update(self):
        result, errors = self._input._validate_item_update(self._form._raw_data)

        self._form._result[self._input.name] = result
        self._form._errors[self._input.name] = errors

        return len(errors) == 0

    def _validate_list_filter(self):
        result, errors = self._input._validate_list_filter(self._form._raw_data)

        self._form._result[self._input.name] = result
        self._form._errors[self._input.name] = errors

        return len(errors) == 0

    def is_valid(self, category):
        return self._form._is_validated and len(self.errors(category)) == 0

    def is_invalid(self, category):
        return self._form._is_validated and len(self.errors(category)) > 0

    def item_select_value(self):
        return self._input._item_select_value(self._form._result)

    def item_select_value_format(self, format=None):
        return self._input._item_select_value_format(self._form._result)

    def item_update_value(self):
        return self._input._item_update_value(self._form._result)

    def item_update_value_format(self, format=None):
        return self._input._item_update_value_format(self._form._result)

    def list_filter_value(self):
        return self._input._list_filter_value(self._form._result)

    def list_filter_value_format(self, format=None):
        return self._input._list_filter_value_format(self._form._result)

    def errors(self, category):
        input_errors = self._form._errors.get(self._input.name, None)

        if input_errors is None:
            return []

        return input_errors.get(category, [])


class BinderMeta(object):
    def __init__(self, inputs, *args, **kwargs):
        self.inputs = inputs


class BinderBase(object):
    def __new__(cls, *args, **kwargs):
        meta_dict = {}
        input_dict = {}

        for base in reversed(cls.__mro__):
            meta_class = getattr(base, 'Meta', None)

            if meta_class and isclass(meta_class):
                for name in dir(meta_class):
                    if not name.startswith('_'):
                        meta_dict[name] = getattr(meta_class, name)
            
            for name in dir(base):
                if not name.startswith('_'):
                    input = getattr(base, name)

                    if not input.name:
                        input.name = name

                    if isinstance(input, InputBase):
                        input_dict[input.name] = input

        result = super().__new__(cls)
        result._meta = BinderMeta(list(input_dict.values()), meta_dict)

        return result

    def __init__(self, prefix='', **kwargs):
        self._prefix = prefix
        self._raw_data = {}
        self._is_validated = False
        self._is_valid = False
        self._result = {}
        self._errors = {}
        self._inputs = []
        self._update(kwargs)

        for inp in self._meta.inputs:
            proxy = InputProxy(self, inp)
            self._inputs.append(proxy)
            setattr(self, inp.name, proxy)

    def _update(self, data):
        self._raw_data = {}
        self._is_validated = False

        for name, value in data.items():
            if name.startswith(self._prefix):
                self._raw_data[name[len(self._prefix):]] = value

    def _validate_item_update(self):
        self._is_validated = True
        self._errors = {}
        self._data = {}
        self._is_valid = True

        for inp in self._inputs:
            # CPython optimizes computation, so operand order is important
            self._is_valid = inp._validate_item_update() and self._is_valid

        return self._is_valid

    def _validate_list_filter(self):
        self._is_validated = True
        self._errors = {}
        self._data = {}
        self._is_valid = True

        for inp in self._inputs:
            # CPython optimizes computation, so operand order is important
            self._is_valid = inp._validate_list_filter() and self._is_valid

        return self._is_valid

    def _get_list_layout(self, request):
        pass

    def _get_item_layout(self, request):
        pass
