from labsystem.auth_app.models import LimsUser
from django.core.validators import MinLengthValidator
from django.db import models

from utils.abstract_models import SoftDeleteModel
from utils.validators import validate_only_letters, validate_value_not_negative


class City(SoftDeleteModel):
    NAME_MAX_LEN = 50
    POST_CODE_MAX_LEN = 20
    MUNICIPALITY_MAX_LEN = 50
    PROVINCE_MAX_LEN = 50
    CODE_MIN_LEN = 2
    CODE_MAX_LEN = 2

    name = models.CharField(
        max_length=NAME_MAX_LEN,
    )

    post_code = models.CharField(
        max_length=POST_CODE_MAX_LEN,
        unique=True,
    )

    municipality = models.CharField(
        max_length=MUNICIPALITY_MAX_LEN,
    )

    province = models.CharField(
        max_length=MUNICIPALITY_MAX_LEN,
    )

    country = models.ForeignKey(
        'Country',
        to_field='code',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Name: {self.name}, province: {self.province}'


class Country(SoftDeleteModel):
    NAME_MAX_LEN = 20
    CODE_MIN_LEN = 2
    CODE_MAX_LEN = 2

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    """
    code according to code Iso2 standard
    """
    code = models.CharField(
        unique=True,
        max_length=CODE_MAX_LEN,
        validators=(
            MinLengthValidator(CODE_MIN_LEN),
        )
    )

    def __str__(self):
        return self.name


class Department(SoftDeleteModel):
    NAME_MAX_LEN = 30
    TELEPHONE_MAX_LEN = 50

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    telephone_number = models.CharField(
        max_length=TELEPHONE_MAX_LEN,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ResultStatus(SoftDeleteModel):
    NAME_MAX_LEN = 20

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    def __str__(self):
        return self.name


class Sample(SoftDeleteModel):
    NAME_MAX_LEN = 30
    CODE_MAX_LEN = 3
    CODE_MIN_LEN = 3

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    code = models.CharField(
        max_length=CODE_MAX_LEN,
        unique=True,
        validators=(
            MinLengthValidator(CODE_MIN_LEN),
        ),
    )

    def __str__(self):
        return self.name


class HealthFacility(SoftDeleteModel):
    NAME_MAX_LEN = 50
    ADDRESS_MAX_LEN = 50
    TELEPHONE_MAX_LEN = 50
    VAT_MAX_LEN = 20
    CONTACT_PERSON_MAX_LEN = 20

    name = models.CharField(
        max_length=NAME_MAX_LEN,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LEN,
    )

    city = models.ForeignKey(
        'City',
        to_field='post_code',
        on_delete=models.CASCADE,
    )

    vat = models.CharField(
        max_length=VAT_MAX_LEN,
        unique=True,
    )

    contact_person = models.CharField(
        max_length=CONTACT_PERSON_MAX_LEN,
    )

    telephone_number = models.CharField(
        max_length=TELEPHONE_MAX_LEN,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    comments = models.TextField(
        blank=True,
        null=True,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} in {self.city}'


class PidType(SoftDeleteModel):
    """
    3 possibilities:
    EGN - Unique Bulgarian citizen identifier
    FPI - Foreign (non Bulgarian) personal identifier
    UIN - Unique Bulgarian physician identifier
    """
    NAME_MAX_LEN = 3

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
        verbose_name='Personal Identifier Type',
        help_text="EGN, FPI or UIN",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Specialty(SoftDeleteModel):
    NAME_MAX_LEN = 50
    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    def __str__(self):
        return self.name


class Position(SoftDeleteModel):
    NAME_MAX_LEN = 50
    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    def __str__(self):
        return self.name


class Sex(SoftDeleteModel):
    NAME_MAX_LEN = 10

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        unique=True,
    )

    def __str__(self):
        return self.name


class Profile(SoftDeleteModel):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    MIDDLE_NAME_MIN_LENGTH = 2
    MIDDLE_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    PID_MAX_LENGTH = 256
    TELEPHONE_MAX_LEN = 20
    ADDRESS_MAX_LEN = 50

    """pid = Personal Identifier (EGN, Personal Number (for foreign citizens) or Doctor's unique identifiers (so 
    called UIN) """
    pid = models.CharField(
        max_length=PID_MAX_LENGTH,
        unique=True,
        verbose_name='Personal Number',
        help_text="Personal Identifier (EGN, Personal Number (for foreign citizens) or Doctor's unique identifiers ("
                  "so called UIN)",
    )

    pid_type = models.ForeignKey(
        PidType,
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    middle_name = models.CharField(
        max_length=MIDDLE_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(MIDDLE_NAME_MIN_LENGTH),
            validate_only_letters,
        ),
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        ),
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    sex = models.ForeignKey(
        Sex,
        on_delete=models.CASCADE,
    )

    telephone_number = models.CharField(
        max_length=TELEPHONE_MAX_LEN,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LEN,
        null=True,
        blank=True,
    )

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    clinical_data = models.TextField(
        null=True,
        blank=True,
    )

    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    health_facility = models.ForeignKey(
        HealthFacility,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    comments = models.TextField(
        null=True,
        blank=True,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(
        LimsUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        mid_name = ''
        if self.middle_name is not None:
            mid_name = ' ' + self.middle_name

        first_second_name = f'{self.first_name}{mid_name}'
        return f'{first_second_name} {self.last_name}'

    def __str__(self):
        return self.full_name

    # """
    # Here, we are telling Django that whenever a save event occurs (signal called post_save)
    # create or save the profile depending on the situation.
    # """
    # @receiver(post_save, sender=LimsUser)
    # def create_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=LimsUser)
    # def save_profile(sender, instance, **kwargs):
    #     instance.profile.save()


class SampleType(SoftDeleteModel):
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 30

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH),
        )
    )

    def __str__(self):
        return self.name


class AnalysisField(SoftDeleteModel):
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 50
    UNIT_MIN_LENGTH = 1
    UNIT_MAX_LENGTH = 10

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH),
        )
    )

    # Measuring units
    unit = models.CharField(
        max_length=UNIT_MAX_LENGTH,
        validators=(
            MinLengthValidator(UNIT_MIN_LENGTH),
        ),
        null=True,
        blank=True,
    )
    male_min = models.FloatField(
        validators=(validate_value_not_negative,),
    )

    male_max = models.FloatField(
        validators=(validate_value_not_negative,),
    )

    female_min = models.FloatField(
        validators=(validate_value_not_negative,),
    )

    female_max = models.FloatField(
        validators=(validate_value_not_negative,),
    )

    # comment when value outside range
    comment = models.TextField(
        null=True,
        blank=True,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Analysis(SoftDeleteModel):
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 30
    CURRENCY_MIN_LENGTH = 3
    CURRENCY_MAX_LENGTH = 3
    PRICE_MAX_DIGITS = 7
    PRICE_DECIMAL_PLACE = 2

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH),
        )
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    currency = models.CharField(
        max_length=CURRENCY_MAX_LENGTH,
        validators=(
            MinLengthValidator(CURRENCY_MIN_LENGTH),
        ),
        default='EUR',
    )

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACE,
        validators=(
            validate_value_not_negative,
        ),
        default=0.00
    )

    tat = models.IntegerField(
        validators=(validate_value_not_negative,)
    )

    analysis_field = models.ManyToManyField(
        AnalysisField,
        blank=True,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Result(SoftDeleteModel):
    CURRENCY_MIN_LENGTH = 3
    CURRENCY_MAX_LENGTH = 3
    PRICE_MAX_DIGITS = 7
    PRICE_DECIMAL_PLACE = 2
    PAYMENT_AMOUNT_MAX_DIGITS = 7
    PAYMENT_AMOUNT_DECIMAL_PLACE = 2

    PAYMENT_BY_CARD = 'PAYMENT_BY_CARD'
    CASH_PAYMENT = 'CASH_PAYMENT'
    PAYMENT_TYPE_NOT_SPECIFIED = 'PAYMENT_TYPE_NOT_SPECIFIED'
    PAYMENT_TYPES = [(x, x) for x in (PAYMENT_BY_CARD, CASH_PAYMENT, PAYMENT_TYPE_NOT_SPECIFIED)]

    patient_id = models.ForeignKey(
        Profile,
        related_name='result_patient_id',
        on_delete=models.CASCADE,
    )

    physician_id = models.ForeignKey(
        Profile,
        related_name='result_physician_id',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    analysis_id = models.ForeignKey(
        Analysis,
        on_delete=models.CASCADE,
    )

    sample_type = models.ForeignKey(
        SampleType,
        on_delete=models.CASCADE,
    )

    sample_collection_time = models.DateField(
        null=True,
        blank=True,
    )

    status = models.ForeignKey(
        ResultStatus,
        on_delete=models.CASCADE,
    )

    analysis_price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACE,
        validators=(
            validate_value_not_negative,
        )
    )

    currency = models.CharField(
        max_length=CURRENCY_MAX_LENGTH,
        validators=(
            MinLengthValidator(CURRENCY_MIN_LENGTH),
        ),
        default='EUR',
    )

    payment_amount = models.DecimalField(
        max_digits=PAYMENT_AMOUNT_MAX_DIGITS,
        decimal_places=PAYMENT_AMOUNT_DECIMAL_PLACE,
        validators=(
            validate_value_not_negative,
        ),
        default=0.00
    )

    payment_type = models.CharField(
        max_length=max(len(x) for x, _ in PAYMENT_TYPES),
        choices=PAYMENT_TYPES,
    )

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'ID: {self.id}, patient ID: {self.patient_id}'


class ResultLine(SoftDeleteModel):
    NAME_MIN_LENGTH = 2
    NAME_MAX_LENGTH = 30

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH),
        )
    )

    value = models.FloatField(
        validators=(validate_value_not_negative,),
        null=True,
        blank=True,
    )

    comment = models.TextField(
        null=True,
        blank=True,
    )

    result_id = models.ForeignKey(
        Result,
        on_delete=models.CASCADE,
    )

    analysis_field_id = models.ForeignKey(
        AnalysisField,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name}'
