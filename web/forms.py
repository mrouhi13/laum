from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='جست‌وجو', min_length=1, max_length=100)
