from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Project, KOL, DataTracking, TrackingNumber
from datetime import datetime


class CustomDateField(serializers.DateField):
    """Custom date field that accepts DD/MM/YYYY format"""
    
    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                # Parse DD/MM/YYYY format
                return datetime.strptime(data, '%d/%m/%Y').date()
            except ValueError:
                try:
                    # Try YYYY-MM-DD format as fallback
                    return datetime.strptime(data, '%Y-%m-%d').date()
                except ValueError:
                    raise serializers.ValidationError(
                        'Date has wrong format. Use DD/MM/YYYY or YYYY-MM-DD format.'
                    )
        return super().to_internal_value(data)
    
    def to_representation(self, value):
        if value:
            return value.strftime('%d/%m/%Y')
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Username must be at least 6 characters long")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined']
        read_only_fields = ['id', 'date_joined']


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Admin API Serializers
class ProjectSerializer(serializers.ModelSerializer):
    created_date = CustomDateField()
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class KOLSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    submitted_on = CustomDateField()
    kol_koc_approval_time = CustomDateField()
    
    class Meta:
        model = KOL
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'project': {'write_only': True, 'required': False}
        }


class DataTrackingSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = DataTracking
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'project': {'write_only': True, 'required': False}
        }


class TrackingNumberSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    tracking_date = CustomDateField()
    
    class Meta:
        model = TrackingNumber
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {
            'project': {'write_only': True, 'required': False}
        } 