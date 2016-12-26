from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# форма для регистрации
from channel.models import Channel


class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин:')
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль:')
    password2 = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Повторите ввод:')
    email = forms.EmailField(label='Email:')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError('Логин уже занят')
        except User.DoesNotExist:
            return username

    def clean_password2(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password2']
        if pass1 != pass2:
            raise forms.ValidationError('Пароли не совпадают, введите одинаковые пароли')

    def save(self):
        user = User()
        data = self.cleaned_data
        user.username = data.get('username')
        user.password = make_password(data.get('password'))
        user.email = data.get('email')
        user.is_active = True
        user.is_superuser = False
        user.save()
        return authenticate(username=user.username, password=user.password)


# форма для авторизации
class AuthorizationForm(forms.Form):
    username = forms.CharField(min_length=5, label='Логин пользователя:')
    password = forms.CharField(min_length=8, widget=forms.PasswordInput, label='Пароль пользователя:')

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('Пользователь неактивен')
        else:
            raise forms.ValidationError('Неверный логин или пароль')


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        exclude = ('author', 'rating')
