from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import * 

@receiver(post_save, sender=NewUser)
def post_save_new_user(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
    else :
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            profile = UserProfile.objects.create(user=instance)
        
@receiver(pre_save, sender=NewUser)
def pre_save_new_user(sender, instance, **kwargs):
    pass