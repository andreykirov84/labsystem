from django import forms
from labsystem.laboratory.models import Profile
from utils.helpers import BootstrapFormMixin


class CreateProfilePatientForm(BootstrapFormMixin, forms.ModelForm):
    result_lines_pk = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):

        # ResultLine
        # name
        # value
        # comment
        # result_id
        # analysis_field_id


        profile = Profile(
            pid=self.cleaned_data['pid'],
            pid_type=self.cleaned_data['pid_type'],
            sex=self.cleaned_data['sex'],
            first_name=self.cleaned_data['first_name'],
            middle_name=self.cleaned_data['middle_name'],
            last_name=self.cleaned_data['last_name'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            telephone_number=self.cleaned_data['telephone_number'],
            email=self.cleaned_data['email'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            clinical_data=self.cleaned_data['clinical_data'],
            comments=self.cleaned_data['comments'],
            user=self.cleaned_data['user'],
        ).save()
        return profile

    class Meta:
        model = Profile
        fields = (
            'pid',
            'pid_type',
            'sex',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'telephone_number',
            'email',
            'address',
            'city',
            'clinical_data',
            'comments',
            'user',
        )
        widgets = {
            'pid': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Personal ID',
                }),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter First Name',
                }),
            'middle_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Middle Name (Optional)',
                }),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Last Name',
                }),
            'user': forms.HiddenInput(
                attrs={
                    'placeholder': 'User id',
                }),
        }

