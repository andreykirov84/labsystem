from django import forms

from labsystem.laboratory.models import Analysis
from utils.abstract_forms import DeleteAbstractForm, RestoreAbstractForm
from utils.helpers import BootstrapFormMixin


class CreateAnalysisForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Analysis
        fields = (
            'code',
            'name',
            'description',
            'price',
            'tat',
        )
        widgets = {
            'code': forms.TextInput(
                attrs={
                    'placeholder': 'Enter analysis code',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter analysis name',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter analysis description',
                }
            ),
        }


class DeleteAnalysisForm(DeleteAbstractForm):
    class Meta:
        model = Analysis
        exclude = (
            'deleted_at',
        )


class RestoreAnalysisForm(RestoreAbstractForm):
    class Meta:
        model = Analysis
        exclude = (
            'deleted_at',
        )
