from django import forms


# TODO - File validation
class UploadFileForm(forms.Form):
    file = forms.FileField()