from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Минимум 8 символов, не простой пароль'
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
