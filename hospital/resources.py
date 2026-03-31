from import_export import fields, resources
from import_export.widgets import DateWidget, ForeignKeyWidget

from .models import Hospital, Patient


class PatientResource(resources.ModelResource):
    hospital = fields.Field(
        column_name='hospital',
        attribute='hospital',
        widget=ForeignKeyWidget(Hospital, 'name'),
    )
    date_of_birth = fields.Field(
        column_name='date_of_birth',
        attribute='date_of_birth',
        widget=DateWidget(format='%Y-%m-%d'),
    )

    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'date_of_birth', 'email', 'hospital')
        export_order = ('first_name', 'last_name', 'date_of_birth', 'email', 'hospital')
        skip_unchanged = True
        report_skipped = True

    def get_instance(self, instance_loader, row):
        return None

    def before_import_row(self, row, **kwargs):
        hospital_name = str(row.get('hospital', '')).strip()
        if hospital_name:
            Hospital.objects.get_or_create(name=hospital_name)
