from django import forms
from .models import CSVFileData

class UploadCSVForm(forms.ModelForm):
    class Meta:
        model = CSVFileData
        fields = ['csv_file']  
        widgets = {
            'csv_file': forms.FileInput(attrs={'accept': '.csv'})  
        }
