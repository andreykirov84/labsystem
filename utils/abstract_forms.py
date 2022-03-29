from django import forms
from django.utils import timezone


class DeleteAbstractForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly = [x for x in self.fields]
        for field in readonly:
            self.fields[field].widget.attrs['readonly'] = 'readonly'
            # self.fields[field].widget = 'forms.TextInput'

    def save(self, commit=True):
        if commit:
            self.instance.deleted_at = timezone.now()
            self.instance.save()
        return self.instance

    class Meta:
        model = None
        exclude = ()


class RestoreAbstractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        readonly = [x for x in self.fields]
        for field in readonly:
            self.fields[field].widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        if commit:
            self.instance.deleted_at = None
            self.instance.save()
        return self.instance

    class Meta:
        model = None
        exclude = ()
