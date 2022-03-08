from django import forms
from acceso.models import *
import re

class UserForm(forms.ModelForm):
#validaciones:
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if len(nombre) < 2:
            self.add_error('nombre', 'El nombre debe contener más de 2 caracteres')
        return nombre
    
    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if len(apellido) < 2:
            self.add_error('apellido', 'El apellido debe contener más de 2 caracteres')
        return apellido
    
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            self.add_error('password', 'El password debe contener más de 8 caracteres')
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirmar_password'):
            raise forms.ValidationError(
                'Las contraseñas no coinciden'
            )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email):
            self.add_error('email', 'El patrón del email no es correcto')
        return email

#campos añadidos al formulario:

    password = forms.CharField(label = "password", max_length=72, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirmar_password = forms.CharField(label = "confirmar_password", max_length=72, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#meta, fields, label, widget

    class Meta:
        model = User
        
        fields = ['nombre', 'apellido', 'email', 'password']
        
        labels = {
            'nombre' : 'Nombre: ',
            'apellido' : 'Apellido: ',
            'email' : 'Correo electrónico: ',
            'password' : 'Contraseña: ',
        }
        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control'}),
            'apellido' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
        }