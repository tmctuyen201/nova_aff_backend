from django.urls import path
from .views import (
    HelloWorldView, 
    RegisterView, 
    LoginView, 
    UserProfileView,
    ProjectListView,
    ProjectDetailView,
    KOLListView,
    KOLDetailView,
    DataTrackingListView,
    DataTrackingDetailView,
    TrackingNumberListView,
    TrackingNumberDetailView,
    # Brand Analytics Views
    BrandDashboardStatsView,
    CreatorListView,
    CreatorDetailView,
    CreatorAnalyticsView,
    VideoAnalyticsView,
    LiveAnalyticsView,
    FollowerDemographicsView,
    TrendDataView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('hello/', HelloWorldView.as_view(), name='hello'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='user_profile'),
    
    # Admin API URLs - sử dụng pk thay vì project_id
    path('admin/projects/', ProjectListView.as_view(), name='project_list'),
    path('admin/projects/<int:project_id>/', ProjectDetailView.as_view(), name='project_detail'),
    
    path('admin/projects/<int:project_id>/kols/', KOLListView.as_view(), name='kol_list'),
    path('admin/projects/<int:project_id>/kols/<int:kol_id>/', KOLDetailView.as_view(), name='kol_detail'),
    
    path('admin/projects/<int:project_id>/data-tracking/', DataTrackingListView.as_view(), name='data_tracking_list'),
    path('admin/projects/<int:project_id>/data-tracking/<int:tracking_id>/', DataTrackingDetailView.as_view(), name='data_tracking_detail'),
    
    path('admin/projects/<int:project_id>/tracking-numbers/', TrackingNumberListView.as_view(), name='tracking_number_list'),
    path('admin/projects/<int:project_id>/tracking-numbers/<int:tracking_id>/', TrackingNumberDetailView.as_view(), name='tracking_number_detail'),
    
    # Brand Analytics API URLs
    path('brand/dashboard/stats/', BrandDashboardStatsView.as_view(), name='brand_dashboard_stats'),
    path('brand/creators/', CreatorListView.as_view(), name='creator_list'),
    path('brand/creators/<int:creator_id>/', CreatorDetailView.as_view(), name='creator_detail'),
    path('brand/creators/<int:creator_id>/analytics/', CreatorAnalyticsView.as_view(), name='creator_analytics'),
    path('brand/creators/<int:creator_id>/video-analytics/', VideoAnalyticsView.as_view(), name='video_analytics'),
    path('brand/creators/<int:creator_id>/live-analytics/', LiveAnalyticsView.as_view(), name='live_analytics'),
    path('brand/creators/<int:creator_id>/demographics/', FollowerDemographicsView.as_view(), name='follower_demographics'),
    path('brand/creators/<int:creator_id>/trends/', TrendDataView.as_view(), name='trend_data'),
]
