from django import forms

from labsystem.laboratory.models import Analysis
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm


class CreateAnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )


class DeleteAnalysisForm(DeleteAbstractForm):
    class Meta:
        model = Analysis
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )


class RestoreAnalysisForm(RestoreAbstractForm):
    class Meta:
        model = Analysis
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )
