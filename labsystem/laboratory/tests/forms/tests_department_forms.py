from django.test import TestCase
import string
import random
from labsystem.laboratory.forms.department_forms import CreateEditDepartmentForm, DeleteDepartmentForm, \
    RestoreDepartmentForm
from labsystem.laboratory.models import Analysis, Department


class TestAnalysisFieldForms(TestCase):
    NAME = 'NAME'
    DESCRIPTION = 'Description'
    TEL_NUMBER = '+359888'
    EMAIL = 'mail@mail.bg'

    def setUp(self):
        Department.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            telephone_number=self.TEL_NUMBER,
            email=self.EMAIL
        )

    def test_CreateEditDepartmentForm__when_empty_form__expect_all_fields_showed(self):
        form = CreateEditDepartmentForm()
        fields = CreateEditDepartmentForm.Meta.fields
        for field in fields:
            self.assertIn(field, form.fields)

    def test__CreateEditDepartmentForm__when_name_long_long__expect_correct_error_message_showed(self):
        letters = string.ascii_letters
        too_long_name_length = Department.NAME_MAX_LEN + 1
        too_long_name = ''.join(random.choice(letters) for i in range(too_long_name_length))
        error_message = f'Ensure this value has at most {Analysis.NAME_MAX_LENGTH} characters (it has {too_long_name_length}).'
        data = {
            'name': too_long_name,
            'description': self.DESCRIPTION,
            'telephone_number': self.TEL_NUMBER,
            'email': self.EMAIL,
        }

        form = CreateEditDepartmentForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['name'].errors[0], error_message)

    def test_CreateEditDepartmentForm__when_name_not_unique__expect_invalid_form_and_correct_error(self):
        # d = Department.objects.first()
        error_message = 'Department with this Name already exists.'
        data = {
            'name': self.NAME,
            'description': self.DESCRIPTION,
            'telephone_number': self.TEL_NUMBER,
            'email': self.EMAIL,
        }

        form = CreateEditDepartmentForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['name'].errors[0], error_message)

    def test_DeleteDepartmentForm__expect_all_fields_showed(self):
        form = DeleteDepartmentForm()
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )
        for field in fields:
            self.assertIn(field, form.fields)

    def test_DeleteAnalysisFieldForm__expect_all_fields_set_to_readonly(self):
        form = DeleteDepartmentForm()
        expect = 'readonly'
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )
        for field in fields:
            actual = form[field].field.widget.attrs[expect]
            self.assertEqual(actual, expect)

    def test_RestoreDepartmentForm__expect_all_fields_showed(self):
        form = RestoreDepartmentForm()
        fields = (
            'name',
            'description',
            'telephone_number',
            'email',
        )
        for field in fields:
            self.assertIn(field, form.fields)

    def test_RestoreDepartmentForm__expect_all_fields_set_to_readonly(self):
        form = RestoreDepartmentForm()
        expect = 'readonly'
        fields = RestoreDepartmentForm.Meta.fields
        for field in fields:
            actual = form[field].field.widget.attrs[expect]
            self.assertEqual(actual, expect)

