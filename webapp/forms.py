from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label='جست‌وجو', max_length=100)
