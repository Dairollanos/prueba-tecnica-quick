from rest_framework import serializers

from .models import Users


class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['username','token']


class UserLoginSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=25)