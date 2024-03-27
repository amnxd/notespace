from django import forms
from django.forms import ClearableFileInput
from .models import UserData


# replace in_input with form input fields css class

class Create_Account_Form(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'User Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

# Form to create accounts
class Login_Form(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



class Notes(forms.Form):
    title = forms.CharField(
        max_length=100,  # Adjust max_length as needed
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Title...',
            'id': 'title_field',
            'class': 'text',  # Updated class name
            'style': 'font-size: 18px; padding: 7px; margin-left: 0%;'
        })
    )

    note = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Type here...',
            'id': 'note_field',
            'class': 'textarea',
            'style': 'width: 70%; height: 300px; font-size: 18px; color: #000000; border-radius: 14px; padding: 10px; background-color: #fff;'
        }),
        required=False
    )
#
# class DeleteNotes(forms.Form):
#     title = forms.CharField(widget=forms.HiddenInput())
#     note = forms.CharField(widget=forms.HiddenInput())