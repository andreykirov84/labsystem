from django import forms


class BootstrapFormMixin:
    fields = {}

    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' form-control'


class DisabledFieldsFormMixin:
    disabled_fields = '__all__'
    fields = {}

    def _init_disabled_fields(self):
        for name, field in self.fields.items():
            if self.disabled_fields != '__all__' and name not in self.disabled_fields:
                continue

            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['disabled'] = 'readonly'
            else:
                field.widget.attrs['readonly'] = 'readonly'


def generate_numerated_tuple_choices_from_list(ll):
    result = []
    max_choice_len = 0
    for x in range(1, len(ll) + 1):
        element = (x, ll[x - 1])
        if len(ll[x - 1]) > max_choice_len:
            max_choice_len = len(ll[x - 1])
        result.append(element)
    return tuple(result), max_choice_len
