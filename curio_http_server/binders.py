from collections import defaultdict
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
        can_item_select=True,
        can_item_update=True,
        can_list_select=True,
        can_list_update=True,
        can_list_filter=False,
        can_list_search=False,
        can_list_sort=False,
        is_readonly=False,
        is_nullable=False,
        verbose_name=None,
        help_text=None,
        choices=None,
        default_item_select=None,
        default_item_update=None,
        default_list_select=None,
        default_list_update=None,
        default_list_filter=None):
        self.name = None
        self.jinja2_macro_name = jinja2_macro_name
        self.attributes = attributes
        self.can_item_select = can_item_select
        self.can_item_update = can_item_update
        self.can_list_select = can_list_select
        self.can_list_update = can_list_update
        self.can_list_filter = can_list_filter
        self.can_list_search = can_list_search
        self.can_list_sort = can_list_sort
        self.is_readonly = is_readonly
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.choices = choices
        self.default_item_select = default_item_select
        self.default_item_update = default_item_update
        self.default_list_select = default_list_select
        self.default_list_update = default_list_update
        self.default_list_filter = default_list_filter


class NullableInputBase(InputBase):
    def __init__(
        self,
        jinja2_macro_name,
        not_null_default,
        is_nullable=False,
        default_item_select=None,
        default_item_update=None,
        default_list_select=None,
        default_list_update=None,
        default_list_filter=None,
        **kwargs):
        if (not is_nullable) and (default_item_select is None):
            default_item_select = not_null_default

        if (not is_nullable) and (default_item_update is None):
            default_item_update = not_null_default

        if (not is_nullable) and (default_list_select is None):
            default_list_select = not_null_default

        if (not is_nullable) and (default_list_update is None):
            default_list_update = not_null_default

        super().__init__(
            jinja2_macro_name,
            default_item_select=default_item_select,
            default_item_update=default_item_update,
            default_list_select=default_list_select,
            default_list_update=default_list_update,
            **kwargs)
        self.is_nullable = is_nullable


class CheckboxInput(InputBase):
    def __init__(self, **kwargs):
        super().__init__('checkbox', **kwargs)

    def _parse_boolean(self, value):
        if value is True or value is False:
            return value

        value = str(value).lower()

        if value in ('t', 'true',  'on',  'yes', '1', 'checked'):
            return True

        if value in ('f', 'false', 'off', 'no',  '0'):
            return False

        return None

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if raw_data is None:
            result = self.default_item_update
        else:
            result = self._parse_boolean(raw_data)

            if result is None:
                errors['value'].append(f'Invalid value ({raw_data}).')

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        raw_data = form_raw_data.get(self.name)

        return self._parse_boolean(raw_data), {'state': []}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        return str(value)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        return str(value)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter
        value  = self._parse_boolean(form_result.get(self.name, default))

        return value

    def _list_filter_value_format(self, form_result, format=None):
        value = self._list_filter_value(form_result)

        return ['' if item is None else str(item) for item in value]


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

    def _parse_date(self, value):
        if value is None:
            return value

        if type(value) is date:
            return value

        if type(value) is datetime:
            return value.date()

        for format in self.formats:
            try:
                return datetime.strptime(value, format).date()
            except ValueError:
                pass

        return None

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            result = self._parse_date(raw_data)

            if result is None:
                errors.append(f'Invalid value ({raw_data}).')
            else:
                if result < self.min_value:
                    errors.append(f'Value ({raw_data}) must be after {self.min_value}.')

                if result > self.max_value:
                    errors.append(f'Value ({raw_data}) must be before {self.max_value}.')

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result_lower = None
        result_upper = None
        errors_lower = []
        errors_upper = []
        raw_data_lower = form_raw_data.get(self.name + ':lower')
        raw_data_upper = form_raw_data.get(self.name + ':upper')

        if raw_data_lower:
            result_lower = self._parse_date(raw_data_lower)

            if result_lower is None:
                errors_lower.append(f'Invalid value ({raw_data_lower}).')

        if raw_data_upper:
            result_upper = self._parse_date(raw_data_upper)

            if result_upper is None:
                errors_upper.append(f'Invalid value ({raw_data_upper}).')

        return [result_lower, result_upper], {'lower': errors_lower, 'upper': errors_upper}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ['', '']

        if format is None:
            return ['' if item is None else str(item) for item in value]

        return ['' if item is None else item.__format__(format) for item in value]


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

    def _parse_datetime(self, value):
        if value is None:
            return value

        if type(value) is datetime:
            return value

        for format in self.formats:
            try:
                return datetime.strptime(value, format)
            except ValueError:
                pass

        return None

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            result = self._parse_datetime(raw_data)

            if result is None:
                errors.append(f'Invalid value ({raw_data}).')
            else:
                if result < self.min_value:
                    errors.append(f'Value ({raw_data}) must be after {self.min_value}.')

                if result > self.max_value:
                    errors.append(f'Value ({raw_data}) must be before {self.max_value}.')

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result_lower = None
        result_upper = None
        errors_lower = []
        errors_upper = []
        raw_data_lower = form_raw_data.get(self.name + ':lower')
        raw_data_upper = form_raw_data.get(self.name + ':upper')

        if raw_data_lower:
            result_lower = self._parse_datetime(raw_data_lower)

            if result_lower is None:
                errors_lower.append(f'Invalid value ({raw_data_lower}).')

        if raw_data_upper:
            result_upper = self._parse_datetime(raw_data_upper)

            if result_upper is None:
                errors_upper.append(f'Invalid value ({raw_data_upper}).')

        return [result_lower, result_upper], {'lower': errors_lower, 'upper': errors_upper}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ['', '']

        if format is None:
            return ['' if item is None else str(item) for item in value]

        return ['' if item is None else item.__format__(format) for item in value]


class EMailInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('email', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            result = raw_data

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (not raw_data is None) or self.is_nullable:
            result = raw_data

        return result, {'value': errors}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)


class FileInput(NullableInputBase):
    def __init__(self, **kwargs):
        super().__init__('file', None, **kwargs)

    def _validate_item_update(self, form_raw_data):
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')

        return raw_data, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        return None, {'value': []}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)


class HiddenInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('hidden', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            result = raw_data

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        return None, {'value': []}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)


class NumberInput(NullableInputBase):
    def __init__(self, min_value=0, max_value=100, decimal_places=2, **kwargs):
        super().__init__('number', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_places = decimal_places
        self.step = 1 / (10 ** decimal_places)

    def _parse_number(self, value):
        if self.decimal_places == 0:
            try:
                return int(value)
            except ValueError:
                return None
        else:
            try:
                return Decimal(value)
            except InvalidOperation:
                return None

        return value

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            result = self._parse_number(raw_data)

            if result is None:
                errors.append(f'Invalid value ({raw_data}).')
            else:
                if result < self.min_value:
                    errors.append(f'Value ({raw_data}) must be greater than {self.min_value}.')

                if result > self.max_value:
                    errors.append(f'Value ({raw_data}) must be less than {self.max_value}.')

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result_lower = None
        result_upper = None
        errors_lower = []
        errors_upper = []
        raw_data_lower = form_raw_data.get(self.name + ':lower')
        raw_data_upper = form_raw_data.get(self.name + ':upper')

        if raw_data_lower:
            result_lower = self._parse_number(raw_data_lower)

            if result_lower is None:
                errors_lower.append(f'Invalid value ({raw_data_lower}).')

        if raw_data_upper:
            result_upper = self._parse_number(raw_data_upper)

            if result_upper is None:
                errors_upper.append(f'Invalid value ({raw_data_upper}).')

        return [result_lower, result_upper], {'lower': errors_lower, 'upper': errors_upper}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ['', '']

        if format is None:
            return ['' if item is None else str(item) for item in value]

        return ['' if item is None else item.__format__(format) for item in value]


class PasswordInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('password', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            result = raw_data

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        return None, {'value': []}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)


class RadioInput(NullableInputBase):
    def __init__(self, **kwargs):
        super().__init__('radio', '', **kwargs)

    def _parse_boolean(self, value):
        if value is True or value is False:
            return value

        value = str(value).lower()

        if value in ('t', 'true',  'on',  'yes', '1', 'checked'):
            return True

        if value in ('f', 'false', 'off', 'no',  '0'):
            return False

        return None

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if raw_data in self.choices:
                result = raw_data
            else:
                errors.append(f'Invalid value ({raw_data}).')

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result = {}
        errors = {}

        for item_name in self.choices:
            if item_name:
                item_raw_data = form_raw_data.get(self.name + ':' + item_name)

                if item_raw_data is None:
                    result[item_name] = False
                else:
                    item_result = self._parse_boolean(item_raw_data)

                    if item_result is None:
                        errors[item_name] = [f'Invalid value ({item_raw_data}).']
                        result[item_name] = False
                    else:
                        result[item_name] = item_result

        return result, errors

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        return self._list_filter_value(form)


class SearchInput(NullableInputBase):
    def __init__(self, max_length=255, **kwargs):
        super().__init__('search', '', **kwargs)
        self.max_length = max_length

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            result = raw_data

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (not raw_data is None) or self.is_nullable:
            result = raw_data

        return result, {'value': errors}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)


class SelectInput(NullableInputBase):
    def __init__(self, size=1, **kwargs):
        super().__init__('select', '', **kwargs)
        self.size = size

    def _parse_boolean(self, value):
        if value is True or value is False:
            return value

        value = str(value).lower()

        if value in ('t', 'true',  'on',  'yes', '1', 'checked'):
            return True

        if value in ('f', 'false', 'off', 'no',  '0'):
            return False

        return None

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if raw_data in self.choices:
                result = raw_data
            else:
                errors.append(f'Invalid value ({raw_data}).')

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result = {}
        errors = {}

        for item_name in self.choices:
            if item_name:
                item_raw_data = form_raw_data.get(self.name + ':' + item_name)

                if item_raw_data is None:
                    result[item_name] = False
                else:
                    item_result = self._parse_boolean(item_raw_data)

                    if item_result is None:
                        errors[item_name] = [f'Invalid value ({item_raw_data}).']
                        result[item_name] = False
                    else:
                        result[item_name] = item_result

        return result, errors

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        return self._list_filter_value(form)


class TextInput(NullableInputBase):
    def __init__(self, rows=1, columns=80, max_length=255, **kwargs):
        super().__init__('text', '', **kwargs)
        self.rows = rows
        self.columns = columns
        self.max_length = max_length

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if len(raw_data) > self.max_length:
                errors.append(f'Length must be less than {self.max_length}.')

            result = raw_data

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (not raw_data is None) or self.is_nullable:
            result = raw_data

        return result, {'value': errors}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)


class TimeInput(NullableInputBase):
    def __init__(self, min_value=time.min, max_value=time.max, formats=('%H:%M:%S', '%H:%M'), **kwargs):
        super().__init__('time', min_value, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.formats = formats

    def _parse_time(self, value):
        if value is None:
            return value

        if type(value) is datetime:
            return value

        for format in self.formats:
            try:
                return datetime.strptime(value, format).time()
            except ValueError:
                pass

        return None

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            result = self._parse_time(raw_data)

            if result is None:
                errors.append(f'Invalid value ({raw_data}).')
            else:
                if result < self.min_value:
                    errors.append(f'Value ({raw_data}) must be after {self.min_value}.')

                if result > self.max_value:
                    errors.append(f'Value ({raw_data}) must be before {self.max_value}.')

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result_lower = None
        result_upper = None
        errors_lower = []
        errors_upper = []
        raw_data_lower = form_raw_data.get(self.name + ':lower')
        raw_data_upper = form_raw_data.get(self.name + ':upper')

        if raw_data_lower:
            result_lower = self._parse_time(raw_data_lower)

            if result_lower is None:
                errors_lower.append(f'Invalid value ({raw_data_lower}).')

        if raw_data_upper:
            result_upper = self._parse_time(raw_data_upper)

            if result_upper is None:
                errors_upper.append(f'Invalid value ({raw_data_upper}).')

        return [result_lower, result_upper], {'lower': errors_lower, 'upper': errors_upper}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ['', '']

        if format is None:
            return ['' if item is None else str(item) for item in value]

        return ['' if item is None else item.__format__(format) for item in value]


class UrlInput(NullableInputBase):
    def __init__(self, **kwargs):
        super().__init__('url', '', **kwargs)

    def _validate_item_update(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (raw_data is None) and (not self.is_nullable):
            errors.append('No value specified.')
        else:
            if len(raw_data) > 8192:
                errors.append(f'Length must be less than 8192.')

            result = raw_data

        return result, {'value': errors}

    def _validate_list_filter(self, form_raw_data):
        result = None
        errors = []
        raw_data = form_raw_data.get(self.name)

        if (not raw_data is None) or self.is_nullable:
            result = raw_data

        return result, {'value': errors}

    def _item_select_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_select_value_format(self, form_result, format=None):
        value = self._item_select_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _item_update_value(self, form_result):
        default = self.default_item_select() if callable(self.default_item_select) else self.default_item_select

        return form_result.get(self.name, default)

    def _item_update_value_format(self, form_result, format=None):
        value = self._item_update_value(form_result)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)

    def _list_filter_value(self, form_result):
        default = self.default_list_filter() if callable(self.default_list_filter) else self.default_list_filter

        return form_result.get(self.name, default)

    def _list_filter_value_format(self, form, format=None):
        value = self._list_filter_value(form)

        if value is None:
            return ''

        if format is None:
            return str(value)

        return value.__format__(format)


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
        self.jinja2_macro_name = 'form'
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
