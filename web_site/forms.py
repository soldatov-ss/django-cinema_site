from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from web_site.models import Reviews


class ReviewForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ['name', 'text', 'rating', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Ваше Имя'}),
            'text': forms.Textarea(attrs={'class': 'form__textarea',  'id':"contactcomment" , 'placeholder': 'Ваш отзыв'}),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': "sign__input", 'placeholder': 'Email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "sign__input", 'placeholder': 'Имя пользователя'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "sign__input", 'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': "sign__input", 'placeholder': 'Подтвердите пароль'}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'sign__input', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'sign__input', 'placeholder': 'Пароль'}))

