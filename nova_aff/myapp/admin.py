from django.contrib import admin
from .models import (
    UserProfile, Project, KOL, DataTracking, TrackingNumber,
    Creator, BrandDashboardStats, CreatorAnalytics, VideoAnalytics, 
    LiveAnalytics, FollowerDemographics, TrendData
)

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'project_id', 'created_by', 'created_date']
    list_filter = ['created_date', 'created_at']
    search_fields = ['name', 'project_id']

@admin.register(KOL)
class KOLAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'project', 'tiktok_id', 'followers', 'submitted_on']
    list_filter = ['project', 'submitted_on', 'brand_approval']
    search_fields = ['full_name', 'tiktok_id', 'email']

@admin.register(DataTracking)
class DataTrackingAdmin(admin.ModelAdmin):
    list_display = ['creator', 'project', 'video_id', 'view', 'gmv', 'upload_time']
    list_filter = ['project', 'created_at']
    search_fields = ['creator', 'video_id', 'creator_id']

@admin.register(TrackingNumber)
class TrackingNumberAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'project', 'phone_number', 'tracking_date', 'phone_check']
    list_filter = ['project', 'tracking_date', 'phone_check']
    search_fields = ['tracking_number', 'phone_number', 'tiktok_id']

# Brand Analytics Admin
@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'username', 'followers_count', 'gender', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['display_name', 'username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BrandDashboardStats)
class BrandDashboardStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'clicks_today', 'orders_today', 'revenue_today']
    list_filter = ['date']
    ordering = ['-date']

@admin.register(CreatorAnalytics)
class CreatorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['creator', 'gmv', 'products_sold', 'gpm', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['creator__display_name', 'creator__username']

@admin.register(VideoAnalytics)
class VideoAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['creator', 'total_videos', 'average_views', 'average_engagement_rate', 'gpm_video']
    list_filter = ['start_date', 'end_date']
    search_fields = ['creator__display_name']

@admin.register(LiveAnalytics)
class LiveAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['creator', 'total_live_sessions', 'average_viewers', 'average_engagement_rate', 'gpm_live']
    list_filter = ['start_date', 'end_date']
    search_fields = ['creator__display_name']

@admin.register(FollowerDemographics)
class FollowerDemographicsAdmin(admin.ModelAdmin):
    list_display = ['creator', 'male_percentage', 'female_percentage', 'snapshot_date']
    list_filter = ['snapshot_date']
    search_fields = ['creator__display_name']

@admin.register(TrendData)
class TrendDataAdmin(admin.ModelAdmin):
    list_display = ['creator', 'date', 'gmv', 'products_sold', 'followers_gained']
    list_filter = ['date']
    search_fields = ['creator__display_name']
    ordering = ['-date']
