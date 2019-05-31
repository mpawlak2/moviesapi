from django import forms


class TopArgsForm(forms.Form):
    date_from = forms.DateField()
    date_to = forms.DateField()
