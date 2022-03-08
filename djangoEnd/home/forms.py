from django import forms

from .models import Spam

class SpamForm(forms.ModelForm):
    class Meta:
        model = Spam
        fields = ['mail_content']
