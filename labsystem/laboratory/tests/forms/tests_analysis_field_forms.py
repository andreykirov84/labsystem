from django.test import TestCase
import string
import random
from labsystem.laboratory.forms.analysis_field_forms import CreateEditAnalysisFieldForm, DeleteAnalysisFieldForm, \
    RestoreAnalysisFieldForm
from labsystem.laboratory.models import AnalysisField


class TestAnalysisFieldForms(TestCase):
    NAME = 'blood'
    UNIT = 'IU/l'
    VALUE = 1
    COMMENT = 'Comment'

    def setUp(self):
        AnalysisField.objects.create(
            name=self.NAME,
            unit=self.UNIT,
            male_min=self.VALUE,
            male_max=self.VALUE,
            female_min=self.VALUE,
            female_max=self.VALUE,
            comment=self.COMMENT,
        )

    def test_CreateEditAnalysisFieldForm__when_empty_form__expect_all_fields_showed(self):
        form = CreateEditAnalysisFieldForm()
        fields = (
            'name',
            'unit',
            'male_min',
            'male_max',
            'female_min',
            'female_max',
            'comment',
        )
        for field in fields:
            self.assertIn(field, form.fields)

    def test_CreateEditAnalysisFieldForm__when_name_too_short__expect_correct_error_message_showed(self):
        letters = string.ascii_uppercase
        too_short_name_length = AnalysisField.NAME_MIN_LENGTH - 1
        too_short_name = ''.join(random.choice(letters) for i in range(too_short_name_length))
        error_message = f'Ensure this value has at least {AnalysisField.NAME_MIN_LENGTH} characters (it has {too_short_name_length}).'
        data = {
            'name': too_short_name,
            'unit': self.UNIT,
            'male_min': self.VALUE,
            'male_max': self.VALUE,
            'female_min': self.VALUE,
            'female_max': self.VALUE,
            'comment': self.COMMENT,
        }

        form = CreateEditAnalysisFieldForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['name'].errors[0], error_message)

    def test_CreateEditAnalysisFieldForm__when_name_long_long__expect_correct_error_message_showed(self):
        letters = string.ascii_uppercase
        too_long_name_length = AnalysisField.NAME_MAX_LENGTH + 1
        too_long_name = ''.join(random.choice(letters) for i in range(too_long_name_length))
        error_message = f'Ensure this value has at most {AnalysisField.NAME_MAX_LENGTH} characters (it has {too_long_name_length}).'
        data = {
            'name': too_long_name,
            'unit': self.UNIT,
            'male_min': self.VALUE,
            'male_max': self.VALUE,
            'female_min': self.VALUE,
            'female_max': self.VALUE,
            'comment': self.COMMENT,
        }

        form = CreateEditAnalysisFieldForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['name'].errors[0], error_message)

    def test_CreateEditAnalysisFieldForm__when_unit_field_is_blank__expect_blank_allowed(self):
        value = ''
        data = {
            'name': self.NAME,
            'unit':  value,
            'male_min': self.VALUE,
            'male_max': self.VALUE,
            'female_min': self.VALUE,
            'female_max': self.VALUE,
            'comment': self.COMMENT,
        }

        form = CreateEditAnalysisFieldForm(data)
        self.assertTrue(form.is_valid())

    def test_CreateEditAnalysisFieldForm__when_unit_long_long__expect_correct_error_message_showed(self):
        letters = string.ascii_uppercase
        too_long_str_length = AnalysisField.UNIT_MAX_LENGTH + 1
        too_long_str = ''.join(random.choice(letters) for i in range(too_long_str_length))
        error_message = f'Ensure this value has at most {AnalysisField.UNIT_MAX_LENGTH} characters (it has {too_long_str_length}).'
        data = {
            'name': self.NAME,
            'unit': too_long_str,
            'male_min': self.VALUE,
            'male_max': self.VALUE,
            'female_min': self.VALUE,
            'female_max': self.VALUE,
            'comment': self.COMMENT,
        }

        form = CreateEditAnalysisFieldForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['unit'].errors[0], error_message)

    def test_CreateEditAnalysisFieldForm__when_fields_male_min_male_max_female_min_and_female_max_are_negative__expect_correct_error_messages_showed(self):
        value = -1
        error_message = 'Value must be equal or larger then 0'
        data = {
            'name': self.NAME,
            'unit': self.UNIT,
            'male_min': value,
            'male_max': value,
            'female_min': value,
            'female_max': value,
            'comment': self.COMMENT,
        }

        form = CreateEditAnalysisFieldForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['male_min'].errors[0], error_message)
        self.assertEqual(form['male_max'].errors[0], error_message)
        self.assertEqual(form['female_min'].errors[0], error_message)
        self.assertEqual(form['female_max'].errors[0], error_message)

    def test_DeleteAnalysisFieldForm__expect_all_fields_showed(self):
        form = DeleteAnalysisFieldForm()
        fields = (
            'name',
            'unit',
            'male_min',
            'male_max',
            'female_min',
            'female_max',
            'comment',
        )
        for field in fields:
            self.assertIn(field, form.fields)

    def test_DeleteAnalysisFieldForm__expect_all_fields_set_to_readonly(self):
        form = DeleteAnalysisFieldForm()
        expect = 'readonly'
        fields = DeleteAnalysisFieldForm.Meta.fields
        for field in fields:
            actual = form[field].field.widget.attrs[expect]
            self.assertEqual(actual, expect)

    def test_RestoreAnalysisFieldForm__expect_all_fields_showed(self):
        form = RestoreAnalysisFieldForm()
        fields = (
            'name',
            'unit',
            'male_min',
            'male_max',
            'female_min',
            'female_max',
            'comment',
        )
        for field in fields:
            self.assertIn(field, form.fields)

    def test_RestoreAnalysisFieldForm__expect_all_fields_set_to_readonly(self):
        form = RestoreAnalysisFieldForm()
        expect = 'readonly'
        fields = RestoreAnalysisFieldForm.Meta.fields
        for field in fields:
            actual = form[field].field.widget.attrs[expect]
            self.assertEqual(actual, expect)

