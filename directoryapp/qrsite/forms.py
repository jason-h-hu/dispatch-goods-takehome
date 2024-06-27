from django import forms

class CSVFileForm(forms.Form):
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'accept': ".csv"})
    )
