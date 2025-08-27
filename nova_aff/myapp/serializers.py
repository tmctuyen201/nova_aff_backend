from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Project, KOL, DataTracking, TrackingNumber, UserProfile,
    Creator, BrandDashboardStats, CreatorAnalytics, VideoAnalytics,
    LiveAnalytics, FollowerDemographics, TrendData
)
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
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, default='creator')

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'role']

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
        role = validated_data.pop('role', 'creator')
        validated_data.pop('confirm_password')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        # Update the user profile with the selected role
        user.profile.role = role
        user.profile.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        role = attrs.get('role')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            
            # Check if role is provided and matches user's role
            if role and hasattr(user, 'profile') and user.profile.role != role:
                raise serializers.ValidationError(f'You are not authorized to login as {role}')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined', 'role']
        read_only_fields = ['id', 'date_joined', 'role']


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


# Brand Analytics Serializers
class CreatorSerializer(serializers.ModelSerializer):
    category_display = serializers.SerializerMethodField()
    gender_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Creator
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_category_display(self, obj):
        """Return display names for categories"""
        category_dict = dict(Creator.CATEGORY_CHOICES)
        return [category_dict.get(cat, cat) for cat in obj.categories]
    
    def get_gender_display(self, obj):
        """Return display name for gender"""
        return obj.get_gender_display() if obj.gender else None


class BrandDashboardStatsSerializer(serializers.ModelSerializer):
    date = CustomDateField()
    
    class Meta:
        model = BrandDashboardStats
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CreatorAnalyticsSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.display_name', read_only=True)
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    start_date = CustomDateField()
    end_date = CustomDateField()
    
    class Meta:
        model = CreatorAnalytics
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class VideoAnalyticsSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.display_name', read_only=True)
    start_date = CustomDateField()
    end_date = CustomDateField()
    
    class Meta:
        model = VideoAnalytics
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class LiveAnalyticsSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.display_name', read_only=True)
    start_date = CustomDateField()
    end_date = CustomDateField()
    
    class Meta:
        model = LiveAnalytics
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class FollowerDemographicsSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.display_name', read_only=True)
    snapshot_date = CustomDateField()
    
    class Meta:
        model = FollowerDemographics
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class TrendDataSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.display_name', read_only=True)
    date = CustomDateField()
    
    class Meta:
        model = TrendData
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class CreatorDetailSerializer(serializers.ModelSerializer):
    """Detailed creator info with all analytics"""
    latest_analytics = serializers.SerializerMethodField()
    latest_video_analytics = serializers.SerializerMethodField()
    latest_live_analytics = serializers.SerializerMethodField()
    latest_demographics = serializers.SerializerMethodField()
    trend_data = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Creator
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_latest_analytics(self, obj):
        latest = obj.analytics.first()
        return CreatorAnalyticsSerializer(latest).data if latest else None
    
    def get_latest_video_analytics(self, obj):
        latest = obj.video_analytics.first()
        return VideoAnalyticsSerializer(latest).data if latest else None
    
    def get_latest_live_analytics(self, obj):
        latest = obj.live_analytics.first()
        return LiveAnalyticsSerializer(latest).data if latest else None
    
    def get_latest_demographics(self, obj):
        latest = obj.follower_demographics.first()
        return FollowerDemographicsSerializer(latest).data if latest else None
    
    def get_trend_data(self, obj):
        trends = obj.trend_data.all()[:30]  # Last 30 days
        return TrendDataSerializer(trends, many=True).data
    
    def get_category_display(self, obj):
        """Return display names for categories"""
        category_dict = dict(Creator.CATEGORY_CHOICES)
        return [category_dict.get(cat, cat) for cat in obj.categories] 