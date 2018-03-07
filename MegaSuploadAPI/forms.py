from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    dirId = forms.UUIDField()

# TODO add login and register form validator
