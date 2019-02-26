from .models import *
from rest_framework import serializers


class LikesSerialisers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['Liked_post_id']

