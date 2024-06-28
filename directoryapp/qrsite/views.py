import qrcode
import io
import csv
from qrsite.forms import CSVFileForm
from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import UserModel
from string import Template

def index(request):
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

def get_user_or_throw(id):
    try:
        user = UserModel.objects.get(id=id)
        return user
    except UserModel.DoesNotExist:
        raise Http404('User does not exist')

def get_qr(request, id):
    host = request.META['HTTP_HOST']
    get_user_or_throw(id)
    qr = qrcode.QRCode()
    qr.add_data(Template('$host/users/$id').substitute(
        host=host,
        id=id
    ))
    img = qr.make_image()
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return HttpResponse(byte_io, content_type='image/png')

def get_user(request, id):
    user = get_user_or_throw(id)
    context={'user': user}
    return render(request, 'user.html', context=context)

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

