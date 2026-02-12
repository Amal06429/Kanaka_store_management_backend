from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UploadedFile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True, required=False)
    plain_password = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'plain_password', 'email', 'role',
            'shop_name', 'staff_name', 'mobile_number',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_plain_password(self, obj):
        """Return plain password only for admin users"""
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'admin':
            return obj.plain_password
        return None
    
    def create(self, validated_data):
        """Create a new user with encrypted password"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
            user.plain_password = password  # Store for admin viewing
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user, handle password separately"""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
            instance.plain_password = password  # Store for admin viewing
        
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating users"""
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'role',
            'shop_name', 'staff_name', 'mobile_number'
        ]
    
    def create(self, validated_data):
        """Create a new user with encrypted password"""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.plain_password = password  # Store for admin viewing
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """Validate username and password"""
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            data['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return data


class UploadedFileSerializer(serializers.ModelSerializer):
    """Serializer for UploadedFile model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)
    file_size_display = serializers.CharField(source='get_file_size_display', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UploadedFile
        fields = [
            'id', 'user', 'user_username', 'user_role', 'name', 'file', 'file_url',
            'file_type', 'file_size', 'file_size_display',
            'heading', 'description', 'document_type', 'amount', 'status', 'uploaded_at', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    
    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None


class FileUploadSerializer(serializers.ModelSerializer):
    """Serializer for file upload"""
    file = serializers.FileField(required=True)
    
    class Meta:
        model = UploadedFile
        fields = ['file', 'heading', 'description', 'document_type', 'amount', 'status', 'uploaded_at']
    
    def create(self, validated_data):
        """Create uploaded file with user from context"""
        file_obj = validated_data.get('file')
        validated_data['name'] = file_obj.name
        validated_data['file_type'] = file_obj.content_type or 'application/octet-stream'
        validated_data['file_size'] = file_obj.size
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
