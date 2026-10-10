from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(label="", max_length=100, required=True)


class AdvanceSearchForm(forms.Form):
    q = forms.CharField(label="", max_length=100, required=True)
