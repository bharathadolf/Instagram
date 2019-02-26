from .models import *
from rest_framework import serializers


class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ProfileSerialisers(serializers.ModelSerializer):
    user = UserSerialiser()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset.select_related('user')
        return queryset

    class Meta:
        model = UserProfile
        fields = ('id', 'display_picture', 'user')
