from django import forms

from labsystem.laboratory.models import AnalysisField
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm


class CreateAnalysisFieldForm(forms.ModelForm):
    class Meta:
        model = AnalysisField
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )


class DeleteAnalysisFieldForm(DeleteAbstractForm):
    class Meta:
        model = AnalysisField
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )


class RestoreAnalysisFieldForm(RestoreAbstractForm):
    class Meta:
        model = AnalysisField
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )
