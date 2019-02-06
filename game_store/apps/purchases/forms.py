from django import forms

class PurchaseForm(forms.Form):
    card_type = forms.ChoiceField(label='Card Type', choices = [(0, 'VISA'), (1, 'MasterCard')])
    card_number = forms.CharField(label='Card Number', required=True, max_length=16)
    expiry_month = forms.CharField(label='Expiration Date', required=True, max_length=2)
    expiry_year = forms.CharField(required=True, max_length=4)
    cvv = forms.CharField(required=True, max_length=3, widget=forms.PasswordInput)
