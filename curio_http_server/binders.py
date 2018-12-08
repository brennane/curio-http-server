from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from decimal import InvalidOperation
from inspect import isclass


class InputBase(object):
    def __init__(
        self,
        jinja2_macro_name,
        attributes={},
        can_sort=False,
        can_filter=False,
        can_search=False,
        is_readonly=False,
        is_nullable=False,
        verbose_name=None,
        help_text=None,
        choices=None,
        default=None):
        self.name = None
        self.jinja2_macro_name = jinja2_macro_name
        self.attributes = attributes
        self.can_sort = can_sort
        self.can_filter = can_filter
        self.can_search = can_search
        self.is_readonly = is_readonly
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.choices = choices
        self.default = default

    def _validate_item_update(self, errors, raw_data):
        pass


class NullableInputBase(InputBase):
    def __init__(
        self,
        jinja2_macro_name,
        not_null_default,
        is_nullable=False,
        default=None,
        **kwargs):

        if (not is_nullable) and (default is None):
            default = not_null_default

        super().__init__(jinja2_macro_name, default=default, **kwargs)
        self.is_nullable = is_nullable

    def _validate_item_update(self, errors, raw_data):
        if (raw_data is None) and (not self.is_nullable):
            errors.append(f'No value specified.')


class CheckboxInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('checkbox', **kwargs)

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if raw_data is None:
            return False
        else:
            raw_data = raw_data.lower()

            if raw_data in ('t', 'true', 'on', 'yes', '1', 'checked'):
                return True
            elif raw_data in ('f', 'false', 'off', 'no', '0'):
                return False
            else:
                errors.append(f'Invalid value.')


class ColorInput(NullableInputBase):
    def __init__(self, **kwargs):
        super().__init__('color', '', **kwargs)

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            # TODO: convert to RGB
            return str(raw_data)


class DateInput(NullableInputBase):
    def __init__(
        self,
        min_value=date.min,
        max_value=date.max,
        formats=('%Y/%m/%d', '%Y-%m-%d'),
        **kwargs):
        super().__init__('date', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.formats = formats

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            value = None

            for format in self.formats:
                try:
                    value = datetime.strptime(raw_data, format).date()
                    break
                except ValueError:
                    pass

            if value is None:
                errors.append(f'Invalid value.')
            else:
                if value < self.min_value:
                    errors.append(f'Value ({value}) must be after {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be before {self.max_value}.')

            return value


class DateTimeInput(NullableInputBase):
    def __init__(
        self,
        min_value=datetime.min,
        max_value=datetime.max,
        formats=(
            '%Y/%m/%d %H:%M', '%Y-%m-%d %H:%M',
            '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S'),
        **kwargs):
        super().__init__('datetime', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.formats = formats

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            value = None

            for format in self.formats:
                try:
                    value = datetime.strptime(raw_data, format)
                    break
                except ValueError:
                    pass

            if value is None:
                errors.append(f'Invalid value.')
            else:
                if value < self.min_value:
                    errors.append(f'Value ({value}) must be after {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be before {self.max_value}.')

            return value


class EMailInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('email', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)


class FileInput(NullableInputBase):
    def __init__(self, **kwargs):
        super().__init__('file', None, **kwargs)

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        return raw_data


class HiddenInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('hidden', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)


class NumberInput(NullableInputBase):
    def __init__(self, min_value=0, max_value=100, decimal_places=2, **kwargs):
        super().__init__('number', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_places = decimal_places
        self.step = 1 / (10 ** decimal_places)

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            value = None

            if self.decimal_places == 0:
                try:
                    value = int(raw_data)

                    if value < self.min_value:
                        errors.append(f'Value ({value}) must be greater than {self.min_value}.')

                    if value > self.max_value:
                        errors.append(f'Value ({value}) must be less than {self.max_value}.')
                except ValueError:
                    errors.append(f'Invalid value.')
            else:
                try:
                    value = Decimal(raw_data)

                    if value < self.min_value:
                        errors.append(f'Value ({value}) must be greater than {self.min_value}.')

                    if value > self.max_value:
                        errors.append(f'Value ({value}) must be less than {self.max_value}.')
                except InvalidOperation:
                    errors.append(f'Invalid value.')

            return value


class PasswordInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('password', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)


class RadioInput(NullableInputBase):
    def __init__(self, **kwargs):
        super().__init__('radio', '', **kwargs)

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            return str(raw_data)


class SearchInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('search', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)


class SelectInput(NullableInputBase):
    def __init__(self, size=1, **kwargs):
        super().__init__('select', '', **kwargs)
        self.size = size

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            return str(raw_data)


class TextInput(NullableInputBase):
    def __init__(self, rows=1, columns=80, max_length=255, **kwargs):
        super().__init__('text', '', **kwargs)
        self.rows = rows
        self.columns = columns
        self.max_length = max_length

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            return str(raw_data)


class TimeInput(NullableInputBase):
    def __init__(self, min_value=time.min, max_value=time.max, formats=('%H:%M:%S', '%H:%M'), **kwargs):
        super().__init__('time', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.formats = formats

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            value = None

            for format in self.formats:
                try:
                    value = datetime.strptime(raw_data, format).time()
                    break
                except ValueError:
                    pass

            if value is None:
                errors.append(f'Invalid value.')
            else:
                if value < self.min_value:
                    errors.append(f'Value ({value}) must be after {self.min_value}.')

                if value > self.max_value:
                    errors.append(f'Value ({value}) must be before {self.max_value}.')

            return value


class UrlInput(NullableInputBase):
    def __init__(self, **kwargs):
        super().__init__('url', '', **kwargs)

    def _validate_item_update(self, errors, raw_data):
        super()._validate_item_update(errors, raw_data)

        if not raw_data is None:
            if len(raw_data) > 8192:
                errors.append(f'Length must be less than 8192.')

            return str(raw_data)


class InputProxy(object):
    def __getattr__(self, name):
        return getattr(self._input, name)

    def __init__(self, form, input):
        self._form = form
        self._input = input

    def _validate_item_update(self):
        errors = []
        self._form._data[self._input.name] = self._input._validate_item_update(errors, self._form._raw_data.get(self._input.name))
        self._form._errors[self._input.name] = errors

        return len(errors) == 0

    def is_valid(self):
        return self._form._is_validated and len(self.errors()) == 0

    def is_invalid(self):
        return self._form._is_validated and len(self.errors()) > 0

    def value(self):
        return self._form._data.get(self._input.name, self._input.default)

    def value_format(self, format=None):
        value = self.value()

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def errors(self):
        return self._form._errors.get(self._input.name, [])


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
        self.jinja2_macro_name = 'form'
        self._prefix = prefix
        self._raw_data = {}
        self._data = {}
        self._is_validated = False
        self._is_valid = False
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

    def _get_list_layout(self, request):
        pass

    def _get_item_layout(self, request):
        pass
