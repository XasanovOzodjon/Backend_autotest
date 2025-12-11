from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'avatar', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},   
            'avatar': {'write_only': True}
        }
        

    def validate(self, attrs):
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email is already in use.")
        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username is already in use.")
        if len(attrs['password']) < 4:
            raise serializers.ValidationError("Password must be at least 4 characters long.")
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

