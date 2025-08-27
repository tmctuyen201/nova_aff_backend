from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    get_tokens_for_user,
    ProjectSerializer,
    KOLSerializer,
    DataTrackingSerializer,
    TrackingNumberSerializer,
    # Brand Analytics Serializers
    CreatorSerializer,
    BrandDashboardStatsSerializer,
    CreatorAnalyticsSerializer,
    VideoAnalyticsSerializer,
    LiveAnalyticsSerializer,
    FollowerDemographicsSerializer,
    TrendDataSerializer,
    CreatorDetailSerializer
)
from .models import (
    Project, KOL, DataTracking, TrackingNumber,
    Creator, BrandDashboardStats, CreatorAnalytics, VideoAnalytics,
    LiveAnalytics, FollowerDemographics, TrendData
)
from datetime import datetime, timedelta
from django.utils import timezone
# Create your views here.


class HelloWorldView(APIView):
    def get(self, request):
        return Response({'message': 'Hello world'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            user_data = UserSerializer(user).data
            
            return Response({
                'message': 'User registered successfully',
                'user': user_data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            user_data = UserSerializer(user).data
            
            return Response({
                'message': 'Login successful',
                'user': user_data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response({
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)


# Admin API Views
class ProjectListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class KOLListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            kols = KOL.objects.filter(project=project)
            serializer = KOLSerializer(kols, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            
            # Handle multipart form data for video upload
            data = request.data.copy()
            
            # Get video file from request.FILES
            if 'video_file' in request.FILES:
                data['video_file'] = request.FILES['video_file']
            
            serializer = KOLSerializer(data=data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class KOLDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id, kol_id):
        try:
            kol = KOL.objects.get(id=kol_id, project_id=project_id)
            serializer = KOLSerializer(kol)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KOL.DoesNotExist:
            return Response({'error': 'KOL not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, project_id, kol_id):
        try:
            kol = KOL.objects.get(id=kol_id, project_id=project_id)
            
            # Handle multipart form data for video upload
            data = request.data.copy()
            
            # Get video file from request.FILES
            if 'video_file' in request.FILES:
                data['video_file'] = request.FILES['video_file']
            
            serializer = KOLSerializer(kol, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KOL.DoesNotExist:
            return Response({'error': 'KOL not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, project_id, kol_id):
        try:
            kol = KOL.objects.get(id=kol_id, project_id=project_id)
            kol.delete()
            return Response({'message': 'KOL deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except KOL.DoesNotExist:
            return Response({'error': 'KOL not found'}, status=status.HTTP_404_NOT_FOUND)


class DataTrackingListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            data_tracking = DataTracking.objects.filter(project=project)
            serializer = DataTrackingSerializer(data_tracking, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            
            # Handle multipart form data for video upload
            data = request.data.copy()
            
            # Get video file from request.FILES
            if 'video_file' in request.FILES:
                data['video_file'] = request.FILES['video_file']
            
            serializer = DataTrackingSerializer(data=data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class DataTrackingDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id, tracking_id):
        try:
            tracking = DataTracking.objects.get(id=tracking_id, project_id=project_id)
            serializer = DataTrackingSerializer(tracking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except DataTracking.DoesNotExist:
            return Response({'error': 'Data tracking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, project_id, tracking_id):
        try:
            tracking = DataTracking.objects.get(id=tracking_id, project_id=project_id)
            
            # Handle multipart form data for video upload
            data = request.data.copy()
            
            # Get video file from request.FILES
            if 'video_file' in request.FILES:
                data['video_file'] = request.FILES['video_file']
            
            serializer = DataTrackingSerializer(tracking, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DataTracking.DoesNotExist:
            return Response({'error': 'Data tracking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, project_id, tracking_id):
        try:
            data_tracking = DataTracking.objects.get(id=tracking_id, project_id=project_id)
            data_tracking.delete()
            return Response({'message': 'Data tracking deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except DataTracking.DoesNotExist:
            return Response({'error': 'Data tracking not found'}, status=status.HTTP_404_NOT_FOUND)


class TrackingNumberListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            tracking_numbers = TrackingNumber.objects.filter(project=project)
            serializer = TrackingNumberSerializer(tracking_numbers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, project_id):
        try:
            project = Project.objects.get(id=project_id)
            
            # Handle multipart form data for video upload
            data = request.data.copy()
            
            print("Request data:", request.data)
            print("Request FILES:", request.FILES)
            
            # Get video file from request.FILES
            if 'video_file' in request.FILES:
                data['video_file'] = request.FILES['video_file']
                print("Video file found:", request.FILES['video_file'])
            else:
                print("No video file in request.FILES")
            
            print("Final data to save:", data)
            
            serializer = TrackingNumberSerializer(data=data)
            if serializer.is_valid():
                serializer.save(project=project)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


class TrackingNumberDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, project_id, tracking_id):
        try:
            tracking = TrackingNumber.objects.get(id=tracking_id, project_id=project_id)
            serializer = TrackingNumberSerializer(tracking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TrackingNumber.DoesNotExist:
            return Response({'error': 'Tracking number not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, project_id, tracking_id):
        try:
            tracking = TrackingNumber.objects.get(id=tracking_id, project_id=project_id)
            
            # Handle multipart form data for video upload
            data = request.data.copy()
            
            # Get video file from request.FILES
            if 'video_file' in request.FILES:
                data['video_file'] = request.FILES['video_file']
            
            serializer = TrackingNumberSerializer(tracking, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TrackingNumber.DoesNotExist:
            return Response({'error': 'Tracking number not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, project_id, tracking_id):
        try:
            tracking_number = TrackingNumber.objects.get(id=tracking_id, project_id=project_id)
            tracking_number.delete()
            return Response({'message': 'Tracking number deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except TrackingNumber.DoesNotExist:
            return Response({'error': 'Tracking number not found'}, status=status.HTTP_404_NOT_FOUND)


# Brand Analytics API Views
class BrandDashboardStatsView(APIView):
    """Get brand dashboard stats"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        today = timezone.now().date()
        try:
            stats = BrandDashboardStats.objects.get(date=today)
            serializer = BrandDashboardStatsSerializer(stats)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BrandDashboardStats.DoesNotExist:
            # Return default stats if none exist for today
            default_stats = {
                'date': today,
                'clicks_today': 0,
                'orders_today': 0,
                'revenue_today': 0
            }
            return Response(default_stats, status=status.HTTP_200_OK)


class CreatorListView(APIView):
    """Get list of creators"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        creators = Creator.objects.all()
        serializer = CreatorSerializer(creators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatorDetailView(APIView):
    """Get detailed creator information with analytics"""
    permission_classes = [AllowAny]
    
    def get(self, request, creator_id):
        try:
            creator = Creator.objects.get(id=creator_id)
            serializer = CreatorDetailSerializer(creator)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Creator.DoesNotExist:
            return Response({'error': 'Creator not found'}, status=status.HTTP_404_NOT_FOUND)


class CreatorAnalyticsView(APIView):
    """Get creator analytics"""
    permission_classes = [AllowAny]
    
    def get(self, request, creator_id):
        try:
            creator = Creator.objects.get(id=creator_id)
            analytics = creator.analytics.all()
            serializer = CreatorAnalyticsSerializer(analytics, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Creator.DoesNotExist:
            return Response({'error': 'Creator not found'}, status=status.HTTP_404_NOT_FOUND)


class VideoAnalyticsView(APIView):
    """Get video analytics for creator"""
    permission_classes = [AllowAny]
    
    def get(self, request, creator_id):
        try:
            creator = Creator.objects.get(id=creator_id)
            video_analytics = creator.video_analytics.all()
            serializer = VideoAnalyticsSerializer(video_analytics, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Creator.DoesNotExist:
            return Response({'error': 'Creator not found'}, status=status.HTTP_404_NOT_FOUND)


class LiveAnalyticsView(APIView):
    """Get live analytics for creator"""
    permission_classes = [AllowAny]
    
    def get(self, request, creator_id):
        try:
            creator = Creator.objects.get(id=creator_id)
            live_analytics = creator.live_analytics.all()
            serializer = LiveAnalyticsSerializer(live_analytics, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Creator.DoesNotExist:
            return Response({'error': 'Creator not found'}, status=status.HTTP_404_NOT_FOUND)


class FollowerDemographicsView(APIView):
    """Get follower demographics for creator"""
    permission_classes = [AllowAny]
    
    def get(self, request, creator_id):
        try:
            creator = Creator.objects.get(id=creator_id)
            demographics = creator.follower_demographics.all()
            serializer = FollowerDemographicsSerializer(demographics, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Creator.DoesNotExist:
            return Response({'error': 'Creator not found'}, status=status.HTTP_404_NOT_FOUND)


class TrendDataView(APIView):
    """Get trend data for creator"""
    permission_classes = [AllowAny]
    
    def get(self, request, creator_id):
        try:
            creator = Creator.objects.get(id=creator_id)
            
            # Get date range from query params
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            
            trend_data = creator.trend_data.all()
            
            if start_date:
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    trend_data = trend_data.filter(date__gte=start_date)
                except ValueError:
                    pass
            
            if end_date:
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                    trend_data = trend_data.filter(date__lte=end_date)
                except ValueError:
                    pass
            
            # Default to last 30 days if no date range specified
            if not start_date and not end_date:
                thirty_days_ago = timezone.now().date() - timedelta(days=30)
                trend_data = trend_data.filter(date__gte=thirty_days_ago)
            
            serializer = TrendDataSerializer(trend_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Creator.DoesNotExist:
            return Response({'error': 'Creator not found'}, status=status.HTTP_404_NOT_FOUND)
