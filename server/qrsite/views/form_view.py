import io
import csv
from django.shortcuts import render
from ..models import UserModel
from django import forms
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

class CSVFileForm(forms.Form):
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': ".csv"})
    )

    def __init__(self, expected_headers=[], *args, **kwargs):
        self.expected_headers = expected_headers
        super().__init__(*args, **kwargs)

    def clean_file(self):
        data_set = self.files['file'].read().decode('utf-8-sig')
        io_string = io.StringIO(data_set)
        csv_reader = csv.DictReader(io_string, delimiter=',', quotechar='"')
        missing_elements = list(set(self.expected_headers) - set(csv_reader.fieldnames))

        if len(missing_elements) > 0:
            raise forms.ValidationError(f"Missing headers in CSV file. Missing '{missing_elements}'")

        misformatted_rows = []
        cleaned_rows = []
        for i, row in enumerate(csv_reader):
            misformatted_headers = [key for key in self.expected_headers if row[key] is None or row[key].strip() == '']
            if (len(misformatted_headers)):
                misformatted_rows.append(i)
            else:
                cleaned_rows.append(row)

        if len(misformatted_rows) > 0:
            raise forms.ValidationError(f"CSV has missing values in rows '{misformatted_rows}'")

        return cleaned_rows

def _handle_request_and_update_users(request):
    if not request.method == 'POST':
        return [CSVFileForm(), []]

    form = CSVFileForm(
        expected_headers=['firstName', 'lastName', 'age', 'address'], 
        data=request.POST, 
        files=request.FILES
    )
    if not form.is_valid():
        return [form, []]
    
    users = [
        UserModel.objects.create(
            first_name=row['firstName'], 
            last_name=row['lastName'], 
            age=row['age'], 
            address=row['address'],
        ) for row in form.cleaned_data['file']
    ]
    return [form, users]

def form_view(request):
    [form , users]= _handle_request_and_update_users(request)
    context = {'form': form, 'user_ids': [user.id for user in users]}
    return render(request, 'index.html', context=context)

@api_view(['POST'])
def api_form_view(request):
    [form , users]= _handle_request_and_update_users(request)
    if form.is_valid():
        return Response({'user_ids': [user.id for user in users]}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)