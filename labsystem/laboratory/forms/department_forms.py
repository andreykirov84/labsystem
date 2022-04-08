from django import forms

from labsystem.laboratory.models import Department
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm
from utils.helpers import BootstrapFormMixin


class CreateEditDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'class': 'form-control'}),
            'telephone_number':  forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class DeleteDepartmentForm(DeleteAbstractForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'class': 'form-control'}),
            'telephone_number':  forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class RestoreDepartmentForm(RestoreAbstractForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea(attrs={'class': 'form-control'}),
            'telephone_number':  forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
