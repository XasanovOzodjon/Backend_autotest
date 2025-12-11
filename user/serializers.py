from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from account.models import CustomUser



class ProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'id', 'username', 'email', 'avatar', 'totalPoints', 'lastActive', 'role']
        
class ProfileUpdateSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_new_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = CustomUser
        fields = ['avatar', 'password', 'new_password', 'confirm_new_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'new_password': {'write_only': True},
            'confirm_new_password': {'write_only': True}
        }
    
    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')
        if new_password or confirm_new_password:
            if new_password != confirm_new_password:
                raise serializers.ValidationError("New passwords do not match.")
            if len(new_password) < 4:
                raise serializers.ValidationError("New password must be at least 4 characters long.")
        return super().validate(attrs)
    
    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('confirm_new_password', None)  # We don't need to store this
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance
    
class Get_all_Users_Serializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'avatar', 'totalPoints', 'lastActive', 'role', 'is_banned']