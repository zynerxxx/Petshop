from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Relajar validaciones: solo longitud mínima
        self.fields['password1'].help_text = 'Mínimo 4 caracteres.'
        self.fields['password2'].help_text = ''
        self.fields['password1'].widget.attrs['minlength'] = 4
        self.fields['password1'].widget.attrs['autocomplete'] = 'new-password'
        self.fields['password2'].widget.attrs['autocomplete'] = 'new-password'
        # Placeholders y clases para todos los campos
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Usuario', 'autocomplete': 'username'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Correo electrónico', 'autocomplete': 'email'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre', 'autocomplete': 'given-name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Apellido', 'autocomplete': 'family-name'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña (mínimo 4 caracteres)'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 4:
            raise forms.ValidationError('La contraseña debe tener al menos 4 caracteres.')
        return password1

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
        }