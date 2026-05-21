from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-input',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-input',
    }))


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect(attrs={
        'class': 'role-radio',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'First Name', 'class': 'form-input',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Last Name', 'class': 'form-input',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address', 'class': 'form-input',
    }))

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'role', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password', 'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password', 'class': 'form-input'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'bio', 'profile_pic')
        widgets = {
            'first_name':  forms.TextInput(attrs={'class': 'form-input'}),
            'last_name':   forms.TextInput(attrs={'class': 'form-input'}),
            'email':       forms.EmailInput(attrs={'class': 'form-input'}),
            'phone':       forms.TextInput(attrs={'class': 'form-input'}),
            'bio':         forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-input'}),
        }