from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random
from myapp.models import (
    Creator, BrandDashboardStats, CreatorAnalytics, VideoAnalytics,
    LiveAnalytics, FollowerDemographics, TrendData
)


class Command(BaseCommand):
    help = 'Seed brand analytics data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed brand analytics data...'))
        
        # Create sample creators
        self.create_creators()
        
        # Create dashboard stats
        self.create_dashboard_stats()
        
        # Create analytics for each creator
        self.create_analytics()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded brand analytics data!'))

    def create_creators(self):
        """Create sample creators"""
        creators_data = [
            {
                'username': 'quynhanh_23291702',
                'display_name': 'Nguyễn Quỳnh Anh',
                'tiktok_url': 'https://www.tiktok.com/@auroracastle2',
                'avatar': '/brand-avatar.png',
                'categories': ['beauty', 'lifestyle'],
                'gender': 'female',
                'followers_count': 762400,
            },
            {
                'username': 'minh_beauty_official',
                'display_name': 'Nguyễn Thị Minh',
                'tiktok_url': 'https://www.tiktok.com/@minh_beauty_official',
                'avatar': '/brand-avatar.png',
                'categories': ['beauty', 'fashion'],
                'gender': 'female',
                'followers_count': 543200,
            },
            {
                'username': 'hoang_tech_review',
                'display_name': 'Trần Văn Hoàng',
                'tiktok_url': 'https://www.tiktok.com/@hoang_tech_review',
                'avatar': '/brand-avatar.png',
                'categories': ['tech', 'education'],
                'gender': 'male',
                'followers_count': 892100,
            }
        ]
        
        for creator_data in creators_data:
            creator, created = Creator.objects.get_or_create(
                username=creator_data['username'],
                defaults=creator_data
            )
            if created:
                self.stdout.write(f'Created creator: {creator.display_name}')

    def create_dashboard_stats(self):
        """Create dashboard stats for recent days"""
        today = timezone.now().date()
        
        for i in range(30):  # Last 30 days
            date_obj = today - timedelta(days=i)
            
            stats, created = BrandDashboardStats.objects.get_or_create(
                date=date_obj,
                defaults={
                    'clicks_today': random.randint(0, 1000),
                    'orders_today': random.randint(0, 50),
                    'revenue_today': Decimal(str(random.randint(0, 1000000)))
                }
            )
            
            if created:
                self.stdout.write(f'Created stats for {date_obj}')

    def create_analytics(self):
        """Create analytics for each creator"""
        creators = Creator.objects.all()
        start_date = date(2025, 6, 30)
        end_date = date(2025, 7, 30)
        
        for creator in creators:
            # Creator Analytics
            analytics_data = {
                'creator': creator,
                'gmv': Decimal(str(random.randint(10000000, 50000000000))),
                'products_sold': random.randint(1000000, 10000000),
                'gpm': Decimal(str(random.randint(50000, 500000))),
                'average_gmv_per_customer': Decimal(str(random.randint(1000000, 10000000))),
                'commission_rate': Decimal('1.00'),
                'total_products': random.randint(100, 1000),
                'price_range_min': Decimal('82000'),
                'price_range_max': Decimal('5000000'),
                'brands_collaborated': random.randint(20, 100),
                'live_gmv_percentage': Decimal(str(random.randint(80, 98))),
                'video_gmv_percentage': Decimal(str(random.randint(1, 10))),
                'product_card_gmv_percentage': Decimal(str(random.randint(1, 5))),
                'category_performance': {
                    'beauty': random.randint(70, 90),
                    'lifestyle': random.randint(5, 15),
                    'other': random.randint(1, 5)
                },
                'start_date': start_date,
                'end_date': end_date
            }
            
            analytics, created = CreatorAnalytics.objects.get_or_create(
                creator=creator,
                start_date=start_date,
                end_date=end_date,
                defaults=analytics_data
            )
            
            if created:
                self.stdout.write(f'Created analytics for {creator.display_name}')

            # Video Analytics
            video_analytics_data = {
                'creator': creator,
                'total_videos': random.randint(10, 50),
                'average_views': random.randint(100000, 1000000),
                'average_engagement_rate': Decimal(str(random.uniform(2.0, 6.0))),
                'gpm_video': Decimal(str(random.randint(100000, 500000))),
                'start_date': start_date,
                'end_date': end_date
            }
            
            video_analytics, created = VideoAnalytics.objects.get_or_create(
                creator=creator,
                start_date=start_date,
                end_date=end_date,
                defaults=video_analytics_data
            )
            
            if created:
                self.stdout.write(f'Created video analytics for {creator.display_name}')

            # Live Analytics
            live_analytics_data = {
                'creator': creator,
                'total_live_sessions': random.randint(20, 80),
                'average_viewers': random.randint(200000, 800000),
                'average_engagement_rate': Decimal(str(random.uniform(1.5, 4.0))),
                'gpm_live': Decimal(str(random.randint(2000000, 5000000))),
                'start_date': start_date,
                'end_date': end_date
            }
            
            live_analytics, created = LiveAnalytics.objects.get_or_create(
                creator=creator,
                start_date=start_date,
                end_date=end_date,
                defaults=live_analytics_data
            )
            
            if created:
                self.stdout.write(f'Created live analytics for {creator.display_name}')

            # Follower Demographics
            demographics_data = {
                'creator': creator,
                'male_percentage': Decimal('26.24'),
                'female_percentage': Decimal('73.76'),
                'age_18_24_percentage': Decimal('32.10'),
                'age_25_34_percentage': Decimal('47.00'),
                'age_35_44_percentage': Decimal('15.50'),
                'age_45_54_percentage': Decimal('3.00'),
                'age_55_plus_percentage': Decimal('2.40'),
                'top_locations': [
                    {'location': 'HỒ CHÍ MINH', 'percentage': 53.4},
                    {'location': 'HÀ NỘI', 'percentage': 18.2},
                    {'location': 'THANH HÓA', 'percentage': 5.2},
                    {'location': 'NGHỆ AN', 'percentage': 4.1},
                    {'location': 'HẢI PHÒNG', 'percentage': 3.7}
                ],
                'snapshot_date': end_date
            }
            
            demographics, created = FollowerDemographics.objects.get_or_create(
                creator=creator,
                snapshot_date=end_date,
                defaults=demographics_data
            )
            
            if created:
                self.stdout.write(f'Created demographics for {creator.display_name}')

            # Trend Data (last 30 days)
            for i in range(30):
                trend_date = end_date - timedelta(days=i)
                
                trend_data = {
                    'creator': creator,
                    'date': trend_date,
                    'gmv': Decimal(str(random.randint(500000000, 2000000000))),
                    'products_sold': random.randint(50000, 200000),
                    'followers_gained': random.randint(100, 2000),
                    'video_views': random.randint(500000, 2000000),
                    'engagement_rate': Decimal(str(random.uniform(2.0, 5.0)))
                }
                
                trend, created = TrendData.objects.get_or_create(
                    creator=creator,
                    date=trend_date,
                    defaults=trend_data
                )
                
                if created and i == 0:  # Only log for the first one to avoid spam
                    self.stdout.write(f'Created trend data for {creator.display_name}')
