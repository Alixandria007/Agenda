from typing import Any
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from contact.models import Contact
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):

    picture = forms.ImageField(
        required= False,
        widget=forms.FileInput(
            attrs={'accept':'image/*',
                   'required': False,}
            )
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'required':False,
        })

        self.fields['last_name'].widget.attrs.update({
            'required':False,
        })

        self.fields['phone'].widget.attrs.update({
            'required':False,
        })

        self.fields['email'].widget.attrs.update({
            'required': False,
        })
        
        

    class Meta:
        model = Contact
        fields = ('first_name','last_name','phone','email','category','description','picture',)
        widgets = {

        }
    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        phone = cleaned_data['phone']
        email = cleaned_data['email']


        fields = cleaned_data.copy()
        required = ['first_name','last_name','phone','email']


        for field,value in fields.items():
            if value == '' and field in required:
                self.add_error(
                    field,
                    ValidationError('Preencha este campo')
                )

        if first_name.isdigit():
            self.add_error(
                'first_name',
                ValidationError('Esse campo não pode ser numerico','invalid')
            )

        if last_name.isdigit():
            self.add_error(
                'last_name',
                ValidationError('Esse campo não pode ser numerico','invalid')
            )

        if phone.isdigit() == False:
            self.add_error(
                'phone',
                ValidationError(
                    'O seu telefone deve ser numerico',
                    code='invalid'
                )
            )

        if '@' not in email:
            self.add_error(
                'email',
                ValidationError(
                    'O Email deve conter um "@"'
                )
            )

        if '.' not in email:
            self.add_error(
                'email',
                ValidationError(
                    'O Email deve conter um "."'
                )
            )
        

        
        return super().clean()


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'required': True,
        })
        self.fields['last_name'].widget.attrs.update({
            'required': True
        })

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email = email).exists():
            self.add_error(
                'email',
                ValidationError('Este email já existe')
            )
            
        return email
    

class RegisterUpdateForm(forms.ModelForm):
    

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'username',
        )

    

    