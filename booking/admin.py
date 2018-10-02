from django.contrib import admin
from booking.models import Company, CompanyAvailability, Booking
from mapwidgets.widgets import GooglePointFieldWidget
from django.contrib.gis.db import models as gis_models
from django.conf import settings


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'active', 'rating']
    readonly_fields = ['rating']
    formfield_overrides = {
        gis_models.PointField: {"widget": GooglePointFieldWidget(settings=settings.MAP_WIDGETS)}
    }


class CompanyAvailabilityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyAvailability, CompanyAvailabilityAdmin)
