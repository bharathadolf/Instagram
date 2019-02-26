from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Posts(models.Model):
    status = models.TextField(blank=True)
    image = models.ImageField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.status


class Likes(models.Model):
    Liked_post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Comments(models.Model):
    comment = models.TextField(max_length=256)
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE)
    commented_post = models.ForeignKey(Posts,on_delete=models.CASCADE)