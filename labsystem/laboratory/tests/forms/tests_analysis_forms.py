from django.test import TestCase
import string
import random
from labsystem.laboratory.forms.analysis_field_forms import RestoreAnalysisFieldForm
from labsystem.laboratory.forms.analysis_forms import CreateEditAnalysisForm, DeleteAnalysisForm, RestoreAnalysisForm
from labsystem.laboratory.models import Analysis


class TestAnalysisFieldForms(TestCase):
    NAME = 'Name'
    VALUE = 1
    COMMENT = 'Comment'
    DESCRIPTION = 'Description'
    CURRENCY = 'EUR'
    PRICE = 1
    TAT = 1

    def setUp(self):
        Analysis.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            currency=self.CURRENCY,
            price=self.PRICE,
            tat=self.TAT,
        )

    def test_CreateEditAnalysisForm__when_empty_form__expect_all_fields_showed(self):
        form = CreateEditAnalysisForm()
        fields = CreateEditAnalysisForm.Meta.fields
        for field in fields:
            self.assertIn(field, form.fields)

    def test_CreateEditAnalysisForm__when_name_too_short__expect_correct_error_message_showed(self):
        letters = string.ascii_uppercase
        too_short_name_length = Analysis.NAME_MIN_LENGTH - 1
        too_short_name = ''.join(random.choice(letters) for i in range(too_short_name_length))
        error_message = f'Ensure this value has at least {Analysis.NAME_MIN_LENGTH} characters (it has {too_short_name_length}).'
        data = {
            'name': too_short_name,
            'description': self.DESCRIPTION,
            'currency': self.CURRENCY,
            'price': self.PRICE,
            'tat': self.TAT,
        }

        form = CreateEditAnalysisForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['name'].errors[0], error_message)

    def test_CreateEditAnalysisForm__when_name_long_long__expect_correct_error_message_showed(self):
        letters = string.ascii_uppercase
        too_long_name_length = Analysis.NAME_MAX_LENGTH + 1
        too_long_name = ''.join(random.choice(letters) for i in range(too_long_name_length))
        error_message = f'Ensure this value has at most {Analysis.NAME_MAX_LENGTH} characters (it has {too_long_name_length}).'
        data = {
            'name': too_long_name,
            'description': self.DESCRIPTION,
            'currency': self.CURRENCY,
            'price': self.PRICE,
            'tat': self.TAT,
        }

        form = CreateEditAnalysisForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['name'].errors[0], error_message)

    def test_CreateEditAnalysisFieldForm__when_description_field_is_blank__expect_blank_allowed(self):
        value = ''
        data = {
            'name': self.NAME,
            'description': value,
            'currency': self.CURRENCY,
            'price': self.PRICE,
            'tat': self.TAT,
        }

        form = CreateEditAnalysisForm(data)
        self.assertTrue(form.is_valid())

    def test_DeleteAnalysisForm__expect_all_fields_showed(self):
        form = DeleteAnalysisForm()
        fields = (
            'name',
            'description',
            'currency',
            'price',
            'tat',
            'analysis_field',
        )
        for field in fields:
            self.assertIn(field, form.fields)

    def test_DeleteAnalysisFieldForm__expect_all_fields_set_to_readonly(self):
        form = DeleteAnalysisForm()
        expect = 'readonly'
        fields = DeleteAnalysisForm.Meta.fields
        for field in fields:
            actual = form[field].field.widget.attrs[expect]
            self.assertEqual(actual, expect)

    def test_RestoreAnalysisForm__expect_all_fields_showed(self):
        form = RestoreAnalysisForm()
        fields = (
            'name',
            'description',
            'currency',
            'price',
            'tat',
            'analysis_field',
        )
        for field in fields:
            self.assertIn(field, form.fields)

    def test_RestoreAnalysisForm__expect_all_fields_set_to_readonly(self):
        form = RestoreAnalysisForm()
        expect = 'readonly'
        fields = RestoreAnalysisForm.Meta.fields
        for field in fields:
            actual = form[field].field.widget.attrs[expect]
            self.assertEqual(actual, expect)

