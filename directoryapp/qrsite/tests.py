from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .views.form_view import CSVFileForm

class CSVFileFormTests(TestCase):
    def test_valid_data(self):
        file = make_test_file([
            ['name', 'age'],
            ['Bob', 12],
            ['Alice', 16],
        ])
        form = CSVFileForm(expected_headers=['name', 'age'], files={'file': file})
        self.assertTrue(form.is_valid())

    def test_superfluous_data(self):
        file = make_test_file([
            ['name', 'age', 'address'],
            ['Bob', 12, '456 Sesame Street'],
            ['Alice', 16, '123 Main Street'],
        ])
        form = CSVFileForm(expected_headers=['name', 'age'], files={'file': file})
        self.assertTrue(form.is_valid())

    def test_missing_key(self):
        file = make_test_file([
            ['name', 'age', 'address'],
            ['Bob', 12],
            ['Alice', 16, '123 Main Street'],
        ])
        form = CSVFileForm(expected_headers=['name', 'age', 'address'], files={'file': file})
        self.assertFalse(form.is_valid())

    def test_null_value(self):
        file = make_test_file([
            ['name', 'age', 'address'],
            ['Bob', 12],
            ['Alice', 16, '123 Main Street'],
        ])
        form = CSVFileForm(expected_headers=['name', 'age', 'address'], files={'file': file})
        self.assertFalse(form.is_valid())

def make_test_file(rows):
    csv_body = '\n'.join([','.join([str(value) for value in row]) for row in rows])
    return SimpleUploadedFile('test.csv', csv_body.encode('utf-8'), content_type='text/csv')
