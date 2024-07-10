from django import forms

from .models import * 
from verification.validators import allow_only_images_validator
# ImageField does not support the custome validators to use the custome validators we should use the fileField
class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class' : 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']