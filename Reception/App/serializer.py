from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from App.models import User, Cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile', 'gender', 'password_hash']

    def update(self, instance, validated_data):
        validated_data['password_hash'] = make_password(validated_data.get('password_hash'))
        super().update(instance, validated_data)
        return instance


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['count']
