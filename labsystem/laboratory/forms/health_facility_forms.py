from django import forms

from labsystem.laboratory.models import HealthFacility
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm


class CreateHealthFacility(forms.ModelForm):
    success_message = "Health facility was created successfully"

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


class DeleteHealthFacilityForm(DeleteAbstractForm):
    class Meta:
        model = HealthFacility
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )


class RestoreHealthFacilityForm(RestoreAbstractForm):
    class Meta:
        model = HealthFacility
        exclude = (
            'created_on',
            'updated_on',
            'deleted_at',
        )
