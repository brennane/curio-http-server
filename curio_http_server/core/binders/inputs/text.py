from .base import NullableInputBase


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
