import io
import csv
from qrsite.forms import CSVFileForm
from django.shortcuts import render
from ..models import UserModel

def form_view(request):
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        # TODO(jason-h-hu): Validate the data
        if form.is_valid():
            users = parse_request_form_file(request)
            context = {'form': form, 'user_ids': [user.id for user in users]}
            return render(request, 'index.html', context=context)
        else:
            # TODO(jason-h-hu): Implement error handling
            print('form isnot valid!')
            print(form.errors)
    
    context = {'form': CSVFileForm()}
    return render(request, 'index.html', context=context)

def parse_request_form_file(request):
    csv_file = request.FILES['file']
    data_set = csv_file.read().decode('utf-8-sig')
    io_string = io.StringIO(data_set)
    csv_reader = csv.DictReader(io_string, delimiter=',', quotechar='"')
    return [
        UserModel.objects.create(
            first_name=row['firstName'], 
            last_name=row['lastName'], 
            age=row['age'], 
            address=row['address'],
        ) for row in csv_reader
    ]
