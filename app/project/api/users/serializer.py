from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """for creating / updating"""
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_staff', 'is_active']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
            is_staff=validated_data['is_staff']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class DisplayUserSerializer(serializers.ModelSerializer):
    """for responses"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'is_staff', 'is_active']
        read_only_fields = ['id']
