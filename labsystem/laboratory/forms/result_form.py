from django import forms
from django.db.models import Q

from labsystem.laboratory.models import Result, Profile, ResultStatus
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm
from utils.widgets import DatePickerInput


class CreateResultForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['referring_physician'].queryset = Profile.objects.filter(user__is_physician=True)
        self.fields['status'].queryset = ResultStatus.objects.filter(Q(name='Registered') | Q(name='Awaiting sample'))

    class Meta:
        model = Result
        exclude = (
            'patient',
            'analysis_price',
            'created_on',
            'updated_on',
            'deleted_at',
        )
        widgets = {
            'sample_collection_time': DatePickerInput(),
        }


class DeleteResultForm(DeleteAbstractForm):
    class Meta:
        model = Result
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )


class RestoreResultForm(RestoreAbstractForm):
    class Meta:
        model = Result
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )
