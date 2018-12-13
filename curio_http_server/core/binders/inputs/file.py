from .base import NullableInputBase


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
