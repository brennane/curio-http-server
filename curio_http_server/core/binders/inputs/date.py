from .base import NullableInputBase
from datetime import date
from datetime import datetime
from datetime import time


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
