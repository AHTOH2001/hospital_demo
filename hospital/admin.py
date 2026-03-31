from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX

from .models import Hospital, Patient
from .resources import PatientResource


class PatientInline(admin.TabularInline):
    model = Patient
    extra = 1


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at')
    search_fields = ('name', 'address')
    inlines = [PatientInline]


@admin.register(Patient)
class PatientAdmin(ImportExportModelAdmin):
    resource_class = PatientResource
    formats = [XLSX]
    import_formats = [XLSX]
    export_formats = [XLSX]
    list_display = ('first_name', 'last_name', 'hospital', 'email')
    list_filter = ('hospital',)
    search_fields = ('first_name', 'last_name', 'email', 'hospital__name')
