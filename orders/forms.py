from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):

    payment_mode = forms.ChoiceField(choices= [
        ('COD', 'Cash on delivery'),
        ('ONLINE_PAYMENT', 'Online payment'),
    ])

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
        'postal_code', 'city']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'first_name',
                'placeholder': 'First Name',
                'required': 'required',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'last_name',
                'placeholder': 'Last Name',
                'required': 'required',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Email',
                'required': 'required',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'id': 'street_address',
                'placeholder': 'Address',
                'required': 'required',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'zipCode',
                'placeholder': 'Zip Code',
                'required': 'required',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'city',
                'placeholder': 'Town',
                'required': 'required',
            }),
        }