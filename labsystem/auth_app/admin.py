from django.contrib import admin

from django.contrib import admin

from labsystem.auth_app.models import LimsUser


@admin.register(LimsUser)
class LimsUserAdmin(admin.ModelAdmin):
    pass
    # inlines = (PetInlineAdmin,)
    # list_display = ('first_name', 'last_name')
