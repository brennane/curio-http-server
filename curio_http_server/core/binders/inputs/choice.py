from .base import NullableInputBase


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
