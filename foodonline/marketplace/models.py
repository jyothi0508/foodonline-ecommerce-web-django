from django.db import models
from verification.models import *
from menu.models import *
# Create your models here.
class cart(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user