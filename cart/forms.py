from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(initial=1,widget=forms.NumberInput(attrs={'class':'no-border','min': 1, 'max': 100}))
    override = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)