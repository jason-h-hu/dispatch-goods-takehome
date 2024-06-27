from django.shortcuts import render
import csv
import io
from qrsite.forms import CSVFileForm
from .models import UserModel

def index(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = CSVFileForm(request.POST, request.FILES)
        # TODO(jason-h-hu): 
        # 1. Validate the data
        if form.is_valid():
            # Initialize a list to store validated rows
            validated_rows = parse_request_form_file(request)
            for row in validated_rows:
                print(row)
            # 2. Create records in the DB
            # 3. Generate the QR codes
            # 4. Profit???
            context = {'form': CSVFileForm(), 'validated_rows': validated_rows}
            return render(request, 'index.html', context=context)
        else:
            print('form isnot valid!')
            print(form.errors)
    
    context = {'form': CSVFileForm()}
    return render(request, 'index.html', context=context)

def parse_request_form_file(request):
    csv_file = request.FILES['file']
    # Read the file and decode it to a string
    data_set = csv_file.read().decode('utf-8-sig')
    # Create a string IO object
    io_string = io.StringIO(data_set)
    csv_reader = csv.DictReader(io_string, delimiter=',', quotechar='"')

    # Initialize a list to store validated rows
    validated_rows = []

    for row in csv_reader:
        user = UserModel.objects.create(
            first_name=row['firstName'], 
            last_name=row['lastName'], 
            age=row['age'], 
            address=row['address'],
        )
        validated_rows.append(user)

    return validated_rows
