from rest_framework import serializers

from .models import Users


class UsersSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=None, allow_blank=False)
    class Meta:
        model = Users
        exclude = ['username','token']


class UserLoginSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25)