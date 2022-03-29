from django import forms

from labsystem.laboratory.models import Position


class CreateJobPositionForm(forms.ModelForm):
    success_message = "Job position was created successfully"

    class Meta:
        model = Position
        fields = '__all__'
