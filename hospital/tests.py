from datetime import date

from django.test import TestCase
from import_export.formats.base_formats import XLSX
from tablib import Dataset

from .models import Hospital, Patient
from .resources import PatientResource


class HospitalPatientModelTests(TestCase):
    def test_patient_belongs_to_hospital(self):
        hospital = Hospital.objects.create(
            name='City Hospital',
            address='123 Main Street',
        )

        patient = Patient.objects.create(
            hospital=hospital,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
        )

        self.assertEqual(patient.hospital, hospital)
        self.assertEqual(hospital.patients.count(), 1)


class PatientImportExportTests(TestCase):
    def test_excel_import_creates_patient_and_hospital(self):
        resource = PatientResource()
        xlsx_format = XLSX()

        dataset = Dataset(headers=['first_name', 'last_name', 'date_of_birth', 'email', 'hospital'])
        dataset.append(['Jane', 'Smith', '1995-04-12', 'jane.smith@example.com', 'Central Clinic'])

        imported_dataset = xlsx_format.create_dataset(xlsx_format.export_data(dataset))
        result = resource.import_data(imported_dataset, dry_run=False)

        self.assertFalse(result.has_errors())
        self.assertTrue(Hospital.objects.filter(name='Central Clinic').exists())
        self.assertTrue(
            Patient.objects.filter(
                first_name='Jane',
                last_name='Smith',
                email='jane.smith@example.com',
                hospital__name='Central Clinic',
            ).exists()
        )

    def test_excel_export_contains_patient_data(self):
        hospital = Hospital.objects.create(name='North Hospital')
        Patient.objects.create(
            hospital=hospital,
            first_name='Alice',
            last_name='Brown',
            date_of_birth=date(1988, 9, 21),
            email='alice.brown@example.com',
        )

        resource = PatientResource()
        xlsx_format = XLSX()
        export_dataset = resource.export()
        imported_dataset = xlsx_format.create_dataset(xlsx_format.export_data(export_dataset))

        self.assertEqual(imported_dataset.headers, ['first_name', 'last_name', 'date_of_birth', 'email', 'hospital'])
        self.assertEqual(imported_dataset[0], ('Alice', 'Brown', '1988-09-21', 'alice.brown@example.com', 'North Hospital'))
