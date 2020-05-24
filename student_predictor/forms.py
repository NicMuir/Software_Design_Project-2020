from django import forms
from django.core.validators import FileExtensionValidator
import pandas as pd
from django.core.exceptions import ValidationError


def file_validator(file):
    # print("Hello")
    try:
        df = pd.read_csv(file)
    except:
        raise ValidationError("An error occurred while reading the csv")

    req_cols = [
        'student_no',
        'first_name',
        'last_name',
        'aggregate_YOS1',
        'aggregate_YOS2',
        'coms_avg_YOS1',
        'coms_avg_YOS2',
        'maths_avg_YOS1',
        'maths_avg_YOS2'
    ]

    if req_cols != list(df.columns):
        raise ValidationError("Columns of file are of wrong format")

    # Puts pointer back at the beginning of the file. read_csv moves the location of the pointer
    file.seek(0)


# TODO - File validation
class UploadFileForm(forms.Form):
    # validator to only allow csv file types
    csv_file_ext_validator = FileExtensionValidator(['csv'], "Only .csv file types are allowed")
    file = forms.FileField(validators=[csv_file_ext_validator, file_validator])  #

    # def clean(self):
    #     file = self.cleaned_data['file']
