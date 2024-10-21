from django import forms 
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shippingFullName = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=True)
    shippingEmail = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=True)
    shippingAddress1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 1'}), required=True)
    shippingAddress2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address 2'}), required=True)
    shippingCity = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
    shippingCounty = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'County'}), required=False)
    shippingPostcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Postcode'}), required=False)
    shippingCountry = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shippingFullName','shippingEmail','shippingAddress1','shippingAddress2','shippingCity','shippingCounty','shippingPostcode','shippingCountry',]
        exclude = ['user',]