from django import forms

from web_site.models import Reviews


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['email', 'name', 'text', 'rating']

