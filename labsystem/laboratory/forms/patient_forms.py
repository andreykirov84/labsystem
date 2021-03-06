from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.models import Profile
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm
from utils.helpers import BootstrapFormMixin
from utils.widgets import DatePickerInput


class CreatePatientUserForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    PASSWORD_LENGTH = 6
    username = forms.CharField(
        max_length=LimsUser.USERNAME_MAX_LENGTH,
    )

    password1 = forms.CharField(
        max_length=PASSWORD_LENGTH,
        widget=forms.TextInput(
            attrs={'placeholder': "Enter password here"})
    )

    password2 = forms.CharField(
        max_length=PASSWORD_LENGTH,
        widget=forms.TextInput(
            attrs={'placeholder': "Enter again the same password here"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password1',
            'password2',
        )


class CreateEditProfilePatientForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
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

            'date_of_birth': DatePickerInput,

            'user': forms.HiddenInput(
                attrs={
                    'placeholder': 'User id',
                }),
        }


class DeletePatientForm(DeleteAbstractForm):
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
                    'class': 'form-control',
                }),

            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter First Name',
                    'class': 'form-control',
                }),

            'middle_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Middle Name (Optional)',
                    'class': 'form-control',
                }),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter Last Name',
                    'class': 'form-control',
                }),

            'date_of_birth': DatePickerInput,

            'user': forms.HiddenInput(
                attrs={
                    'placeholder': 'User id',
                    'class': 'form-control',
                }),
        }


class RestorePatientForm(RestoreAbstractForm):
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

            'date_of_birth': DatePickerInput,

            'user': forms.HiddenInput(
                attrs={
                    'placeholder': 'User id',
                }),
        }
