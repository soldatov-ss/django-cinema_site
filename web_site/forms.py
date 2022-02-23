from django import forms

from web_site.models import Reviews


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['email', 'name', 'text', 'rating']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'Ваш email'}),
            'name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Ваше Имя'}),
            'text': forms.Textarea(attrs={'class': 'form__textarea',  'id':"contactcomment" , 'placeholder': 'Ваш отзыв'}),
        }
