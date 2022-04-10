from django.core.exceptions import ValidationError
from django.test import TestCase
import random
from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.models import Profile, PidType, Sex, Specialty, HealthFacility, Position, Department, City, \
    Country, Analysis, SampleType, ResultStatus, Result, ResultLine, AnalysisField


class ResultLineTests(TestCase):
    NAME = 'Name'
    VALUE = 1
    COMMENT = 'Comment'
    DESCRIPTION = 'Description'
    CURRENCY = 'EUR'
    PRICE = 1
    TAT = 1
    POSITIVE_VALUE = 1
    ZERO_VALUE = 0
    NEGATIVE_VALUE = -1
    PAYMENT_TYPE = 'Cash payment'
    UNIT = 'IU/l'

    def setUp(self):
        country = Country.objects.create(name='Bulgaria', code='BG')
        city = City.objects.create(
            name='Sofia',
            post_code=1000,
            municipality='Sofia',
            province='Sofia',
            country=country,
        )
        hf = HealthFacility.objects.create(
            name='Name',
            address='Address',
            city=city,
            vat='BG11111',
            contact_person='John Doe',
            telephone_number='+359111',
            email='hf_contact@mail.bg',
            comments='Comments',
        )
        pt = PidType.objects.create(
            name='EGN',
        )
        sex = Sex.objects.create(
            name='Male',
        )
        speciality = Specialty.objects.create(
            name='Cardiology',
        )
        position = Position.objects.create(
            name='CTO',
        )
        department = Department.objects.create(
            name='IT',
            description='IT',
            telephone_number='+359555555',
            email='department@mail.bg'
        )
        user = LimsUser.objects.create(
            username='patient',
            is_staff=False,
            is_physician=False,
            is_patient=True,
        )

        analysis = Analysis.objects.create(
            name=self.NAME,
            description=self.DESCRIPTION,
            currency=self.CURRENCY,
            price=self.PRICE,
            tat=self.TAT,
        )

        sample_type = SampleType.objects.create(
            name=self.NAME,
        )

        status = ResultStatus.objects.create(
            name='Ready',
        )

        profile = Profile.objects.create(
            pid=random.randint(1000, 20000),
            pid_type=pt,
            first_name='FirstName',
            middle_name='MiddleName',
            last_name='LastName',
            date_of_birth='1980-03-03',
            sex=sex,
            telephone_number='+359888888',
            email='mail@mail.bg',
            address='1 Address str',
            city=city,
            clinical_data='Clinical Data',
            specialty=speciality,
            health_facility=hf,
            position=position,
            department=department,
            salary=100,
            comments='Comment',
            user=user
        )

        result = Result.objects.create(
            patient=profile,
            referring_physician=profile,
            analysis=analysis,
            sample_type=sample_type,
            status=status,
            analysis_price=self.POSITIVE_VALUE,
            currency=self.CURRENCY,
            payment_amount=self.POSITIVE_VALUE,
            payment_type=self.PAYMENT_TYPE,
        )
        af = AnalysisField.objects.create(
            name=self.NAME,
            unit=self.UNIT,
            male_min=self.VALUE,
            male_max=self.VALUE,
            female_min=self.VALUE,
            female_max=self.VALUE,
            comment=self.COMMENT,
        )
        ResultLine.objects.create(
            name=self.NAME,
            value=self.POSITIVE_VALUE,
            result=result,
            analysis_field=af,
        )

    def test_result_line_str__when_valid_fields__expect_correct_str_method_result(self):
        rl = ResultLine.objects.get(name=self.NAME)
        expected = self.NAME
        actual = rl.__str__()
        self.assertEqual(expected, actual)

    def test_result_line_value_field_validator__when_value_positive__expect_correctly_set_field(self):
        rl = ResultLine.objects.get(name=self.NAME)
        rl.value = self.POSITIVE_VALUE
        rl.full_clean()
        rl.save()
        expected = self.POSITIVE_VALUE
        actual = rl.value
        self.assertEqual(expected, actual)

    def test_result_line_value_field_validator__when_value_is_zero__expect_correctly_set_field(self):
        rl = ResultLine.objects.get(name=self.NAME)
        rl.value = self.ZERO_VALUE
        rl.full_clean()
        rl.save()
        expected = self.ZERO_VALUE
        actual = rl.value
        self.assertEqual(expected, actual)

    def test_result_field_analysis_price_validator__when_value_is_negative__expect_validation_error(self):
        rl = ResultLine.objects.get(name=self.NAME)
        rl.value = self.NEGATIVE_VALUE
        with self.assertRaises(ValidationError):
            rl.full_clean()
