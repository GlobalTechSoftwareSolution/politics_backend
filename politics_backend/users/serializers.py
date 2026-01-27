from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PendingInfo, ActiveInfo

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'role', 'is_approved', 'is_user', 'is_superuser', 'created_at', 'approval_date']
        read_only_fields = ['id', 'is_approved', 'is_user', 'is_superuser', 'created_at', 'approval_date']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'fullname', 'role']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_approved']
        read_only_fields = ['is_approved']


class PendingInfoSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer(read_only=True)
    
    class Meta:
        model = PendingInfo
        fields = ['id', 'heading', 'description', 'image', 'submitted_by', 'submitted_at', 'status']
        read_only_fields = ['id', 'submitted_by', 'submitted_at', 'status']


class ActiveInfoSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    
    class Meta:
        model = ActiveInfo
        fields = ['id', 'heading', 'description', 'image', 'submitted_by', 'approved_by', 'approved_at', 'created_at']
        read_only_fields = ['id', 'submitted_by', 'approved_by', 'approved_at', 'created_at']
