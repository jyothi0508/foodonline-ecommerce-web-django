from django.db import models

from verification.models import *

# Create your models here.

class Vendor(models.Model):

    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, blank=True, null=True)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
