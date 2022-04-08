from django import forms

from labsystem.laboratory.models import AnalysisField
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm


class CreateEditAnalysisFieldForm(forms.ModelForm):
    class Meta:
        model = AnalysisField
        fields = (
            'name',
            'unit',
            'male_min',
            'male_max',
            'female_min',
            'female_max',
            'comment',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'male_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'male_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'female_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'female_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),

        }


class DeleteAnalysisFieldForm(DeleteAbstractForm):
    class Meta:
        model = AnalysisField
        fields = (
            'name',
            'unit',
            'male_min',
            'male_max',
            'female_min',
            'female_max',
            'comment',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'male_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'male_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'female_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'female_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),

        }


class RestoreAnalysisFieldForm(RestoreAbstractForm):
    class Meta:
        model = AnalysisField
        fields = (
            'name',
            'unit',
            'male_min',
            'male_max',
            'female_min',
            'female_max',
            'comment',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'male_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'male_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'female_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'female_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),

        }
