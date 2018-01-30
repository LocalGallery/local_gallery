from bootstrap4.renderers import FieldRenderer


class BetterFieldRenerer(FieldRenderer):

    def get_form_group_class(self):
        return super().get_form_group_class() + f' fld_{self.field.name}'
