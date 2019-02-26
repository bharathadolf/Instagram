from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.TextField(max_length=100, default=" ")
    city = models.CharField(max_length=30, default="")
    phone = PhoneNumberField()
    display_picture = models.ImageField(default="default_dp.png", blank=True, upload_to="user_display_pictures",)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
         user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Follow(models.Model):
    following = models.ForeignKey(User, related_name='following',on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.time)