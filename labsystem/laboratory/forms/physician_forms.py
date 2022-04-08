from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.models import Profile
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm
from utils.helpers import BootstrapFormMixin
from utils.widgets import DatePickerInput


class CreatePhysicianUserForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    PASSWORD_MAX_LENGTH = 10
    username = forms.CharField(
        max_length=LimsUser.USERNAME_MAX_LENGTH,
    )

    password1 = forms.CharField(
        max_length=PASSWORD_MAX_LENGTH,
        widget=forms.PasswordInput()
    )

    password2 = forms.CharField(
        max_length=PASSWORD_MAX_LENGTH,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_physician = True
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password1',
            'password2',
        )


class CreateProfilePhysicianForm(BootstrapFormMixin, forms.ModelForm):
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
            specialty=self.cleaned_data['specialty'],
            health_facility=self.cleaned_data['health_facility'],
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
            'specialty',
            'health_facility',
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


class EditProfilePhysicianForm(BootstrapFormMixin, forms.ModelForm):
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
            'specialty',
            'health_facility',
            'comments',
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

            'telephone_number': forms.TextInput(attrs={'class': 'form-control'}),

            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            'address': forms.TextInput(attrs={'class': 'form-control'}),

            'comments': forms.Textarea(attrs={'class': 'form-control'}),
        }


class DeletePhysicianForm(DeleteAbstractForm):
    class Meta:
        model = Profile
        exclude = (
            'deleted_at',
        )


class RestorePhysicianForm(RestoreAbstractForm):
    class Meta:
        model = Profile
        exclude = (
            'deleted_at',
        )
