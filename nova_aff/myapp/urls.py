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
    TrackingNumberDetailView
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
]
