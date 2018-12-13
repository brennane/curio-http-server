from .base import InputBase


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
