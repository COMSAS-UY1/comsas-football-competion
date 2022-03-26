from django import forms
from .models import ContactInfo
from django.forms.widgets import CheckboxInput, EmailInput, FileInput, NumberInput, PasswordInput, Select, TextInput, Textarea


# Create your forms below.
class ContactForm(forms.ModelForm):
    # Meta data
    class Meta:
        model  = ContactInfo

        # Form fields
        fields = [
            'name',
            'email',
            'phone',
            'subject',
            'message'
        ]

        # Definition of widgets
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nom et Prénom',
                }
            ),

            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your email address',
                }
            ),

            'phone': TextInput(
                attrs={
                    'class': 'form-control w-75',
                    'placeholder': 'Téléphone (Ex. 699887755)',
                }
            ),

            'subject': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Message Subject...',
                }
            ),

            'message': Textarea(
                attrs={
                    'cols': '30',
                    'rows': '10',
                    'class': 'form-control',
                    'placeholder': 'Ecrivez votre message...',
                }
            ),
        }