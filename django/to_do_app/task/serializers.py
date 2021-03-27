
from .models import (Task,User)

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserLoginSerializer(serializers.Serializer):
    email       = serializers.CharField(max_length=255)
    password    = serializers.CharField(max_length=128, write_only=True)
    token       = serializers.CharField(max_length=255, read_only=True)
    full_name   = serializers.CharField(max_length=255, read_only=True)
    branch      = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Girilen  bigilerle ilişkili kullanıcı bulunamadı'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'E-mail veya parola hatalı.'
            )
        return {
            'email' : user.email,
            'token' : jwt_token,
            'full_name' : user.get_full_name(),
        }



class TaskSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    completed_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    created_by = serializers.SerializerMethodField('get_created_by')

    def get_created_by(self,obj):
        return obj.created_by.get_full_name()

    class Meta:
        model   = Task
        fields  = ['id','assigned_user','title','description','created_at','completed_at','created_by','status']
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model   = User
        fields  = ['id','email','get_full_name']



