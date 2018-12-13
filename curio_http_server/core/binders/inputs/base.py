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
