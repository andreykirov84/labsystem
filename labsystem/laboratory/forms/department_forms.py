from django import forms

from labsystem.laboratory.models import Department
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm


class CreateDepartmentForm(forms.ModelForm):
    success_message = "Department was created successfully"

    class Meta:
        model = Department
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )


class DeleteDepartmentForm(DeleteAbstractForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )


class RestoreDepartmentForm(RestoreAbstractForm):
    class Meta:
        model = Department
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )
