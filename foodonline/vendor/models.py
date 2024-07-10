from django.db import models

from verification.models import *
from verification.utils import send_is_approval_email
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
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            orig = Vendor.objects.get(pk = self.pk)
            context = {
                        'user' : self.user,
                        'is_approved': self.is_approved
                    }
            if orig.is_approved !=  self.is_approved:
                if self.is_approved == True :
                    mail_subject = 'Congragulations! Your Restuarent is approved by our admin team'
                    send_is_approval_email( mail_subject, context)
                    
                else :
                    mail_subject = 'Sorry! Your Restuarent is not approved by our admin team '
                    
                    send_is_approval_email( mail_subject, context)
        return super(Vendor, self).save(*args, **kwargs)
    
