from django import forms


class TopArgsForm(forms.Form):
    date_from = forms.DateField()
    date_to = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()

        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")

        if date_from and date_to:
            if date_from > date_to:
                raise forms.ValidationError("The date_from date must be before the date_to date.")

        return cleaned_data
