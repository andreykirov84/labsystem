from django import forms

from labsystem.laboratory.models import Analysis
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm


class CreateEditAnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = (
            'name',
            'description',
            'currency',
            'price',
            'tat',
            'analysis_field',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tat': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DeleteAnalysisForm(DeleteAbstractForm):
    class Meta:
        model = Analysis
        fields = (
            'name',
            'description',
            'currency',
            'price',
            'tat',
            'analysis_field',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tat': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RestoreAnalysisForm(RestoreAbstractForm):
    class Meta:
        model = Analysis
        fields = (
            'name',
            'description',
            'currency',
            'price',
            'tat',
            'analysis_field',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'tat': forms.TextInput(attrs={'class': 'form-control'}),
        }
