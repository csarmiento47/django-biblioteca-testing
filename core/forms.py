
from django import forms
from .models import *
from datetime import datetime

from django.contrib.auth.models import User, Group


class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = '__all__'
        widgets = {
            'autor': forms.TextInput(attrs={'class':'form-control'}),
            'pais': forms.TextInput(attrs={'class':'form-control'})
        }


class LibroForm(forms.ModelForm):

    fecha_publicacion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'dd/mm/yyyy'})
    )

    class Meta:
        model = Libro
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'idioma':forms.Select(attrs={'class':'form-control'}),
            'paginas': forms.NumberInput(attrs={'class':'form-control'}),
            'autores': forms.SelectMultiple(attrs={'class':'form-control','size':10})
        }


    def clean_fecha_publicacion(self):
        fecha = self.cleaned_data.get('fecha_publicacion')

        try:
            return datetime.strptime(fecha, '%d/%m/%Y').date()
        except ValueError:
            raise forms.ValidationError(
                'Formato de fecha inválido. Use dd/mm/yyyy'
            )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk and self.instance.fecha_publicacion:
            self.initial['fecha_publicacion'] = (self.instance.fecha_publicacion.strftime('%d/%m/%Y'))



class RegistroUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password1') != cleaned.get('password2'):
            self.add_error('password2', 'Las contraseñas no coinciden')
        return cleaned
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
            group = Group.objects.get(name='lector')
            user.groups.add(group)

        return user
