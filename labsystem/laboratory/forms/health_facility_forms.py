from django import forms

from labsystem.laboratory.models import HealthFacility
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm
from utils.helpers import BootstrapFormMixin


class CreateEditHealthFacilityForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = HealthFacility

        fields = (
            'name',
            'vat',
            'address',
            'city',
            'contact_person',
            'telephone_number',
            'email',
            'comments',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Facility Name',
                    'class': 'form-control',
                }),
            'vat': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Value-Added Tax Number',
                    'class': 'form-control',
                }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),

            'contact_person': forms.TextInput(
                attrs={
                    'placeholder': 'Contact Person Name',
                    'class': 'form-control',
                }),

            'telephone_number': forms.TextInput(attrs={'class': 'form-control'}),

            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }


class DeleteHealthFacilityForm(DeleteAbstractForm):
    class Meta:
        model = HealthFacility

        fields = (
            'name',
            'vat',
            'address',
            'city',
            'contact_person',
            'telephone_number',
            'email',
            'comments',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Facility Name',
                    'class': 'form-control',
                }),
            'vat': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Value-Added Tax Number',
                    'class': 'form-control',
                }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),

            'contact_person': forms.TextInput(
                attrs={
                    'placeholder': 'Contact Person Name',
                    'class': 'form-control',
                }),

            'telephone_number': forms.TextInput(attrs={'class': 'form-control'}),

            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }


class RestoreHealthFacilityForm(RestoreAbstractForm):
    class Meta:
        model = HealthFacility

        fields = (
            'name',
            'vat',
            'address',
            'city',
            'contact_person',
            'telephone_number',
            'email',
            'comments',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Facility Name',
                    'class': 'form-control',
                }),
            'vat': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Value-Added Tax Number',
                    'class': 'form-control',
                }),
            'address': forms.TextInput(attrs={'class': 'form-control'}),

            'contact_person': forms.TextInput(
                attrs={
                    'placeholder': 'Contact Person Name',
                    'class': 'form-control',
                }),

            'telephone_number': forms.TextInput(attrs={'class': 'form-control'}),

            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }
