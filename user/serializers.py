from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
class CreateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['first_name','family_name','last_name','password','email',]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value: str):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class TokenTestSerializers(TokenObtainPairSerializer):
    username_field = 'email'
    @classmethod
    def get_token(cls, user) -> Token:
        if user.is_active:
            token = super().get_token(user)
            token['role'] = user.role
            return token
        raise AuthenticationFailed("'Аккаунт деактивирован'")
#     "email": "ivan@example.com",
    #"password": "Str0ngP@ssw0rd123",
    
class UpdateUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','family_name','last_name',]
        reat_only_fields = ['email','role',]
