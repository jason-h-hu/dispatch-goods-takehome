from django.shortcuts import render
from qrsite.forms import CSVFileForm

def index(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CSVFileForm(request.POST)

        # TODO(jason-h-hu): 
        # 1. Validate the data
        # 2. Create records in the DB
        # 3. Generate the QR codes
        # 4. Profit???

        context = {'form': form}
        return render(request, 'index.html', context=context)

    
    context = {'form': CSVFileForm()}
    return render(request, 'index.html', context=context)
