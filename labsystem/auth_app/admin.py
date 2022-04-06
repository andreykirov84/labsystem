from django.contrib import admin

from django.contrib import admin

from labsystem.auth_app.models import LimsUser
from labsystem.laboratory.models import Profile, Country, City, Department, ResultStatus, HealthFacility, PidType, \
    Specialty, Position, Sex, SampleType, AnalysisField, Analysis, Result, ResultLine, Sample


class SoftDeletionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()

    def soft_delete_model(self, request, obj):
        obj.soft_delete()


@admin.register(LimsUser)
class LimsUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'is_staff',
        'is_physician',
        'is_patient',
        'is_active',
        'deleted_at',
    )


# @admin.register(City)
class CityAdmin(admin.TabularInline):
    model = City

    list_display = (
        'name',
        'post_code',
        'municipality',
        'province',
        'country',
    )


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    # model = Country
    list_display = (
        'name',
        'code',
    )
    inlines = (
        CityAdmin,
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'telephone_number',
        'email',

    )


@admin.register(ResultStatus)
class ResultStatusAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(HealthFacility)
class HealthFacilityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'city',
        'vat',
        'contact_person',
        'telephone_number',
        'email',
        'comments',
    )


@admin.register(PidType)
class PidTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'pid',
        'pid_type',
        'first_name',
        'middle_name',
        'last_name',
        'date_of_birth',
        'sex',
        'telephone_number',
        'email',
        'address',
        'city',
        'clinical_data',
        'specialty',
        'health_facility',
        'position',
        'department',
        'salary',
        'comments',
        'user',
    )


@admin.register(SampleType)
class SampleTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(AnalysisField)
class AnalysisFieldAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'unit',
        'male_min',
        'male_max',
        'female_min',
        'female_max',
        'comment',
    )


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'currency',
        'price',
        'tat',
        # 'analysis_field',
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'referring_physician',
        'analysis',
        'sample_type',
        'sample_collection_time',
        'status',
        'analysis_price',
        'currency',
        'payment_amount',
        'payment_type',
    )


@admin.register(ResultLine)
class ResultLineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'value',
        'comment',
        'result',
        'analysis_field',
    )


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'result',
    )
