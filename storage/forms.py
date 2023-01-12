from django import forms

from storage.models import File


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['folder', 'title', 'description', 'file', 'hidden', 'teacher', 'speciality']
