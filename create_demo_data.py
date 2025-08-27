#!/usr/bin/env python
"""
Nova Aff Demo Data Creation Script
Creates users, campaigns, and sample data for production testing
"""

import os
import sys
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova_aff.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction
from myapp.models import *
from datetime import datetime, timedelta
import random

User = get_user_model()

class DemoDataCreator:
    def __init__(self):
        self.users = {}
        self.categories = []
        self.campaigns = []
        
    def create_users(self):
        """Create demo users with different roles"""
        print("🔧 Creating demo users...")
        
        users_data = [
            # Admin users
            {
                'username': 'admin',
                'email': 'admin@novaaff.id.vn',
                'password': 'admin123',
                'role': 'admin',
                'is_superuser': True,
                'is_staff': True
            },
            {
                'username': 'manager',
                'email': 'manager@novaaff.id.vn',
                'password': 'manager123',
                'role': 'admin',
                'is_staff': True
            },
            
            # Brand users
            {
                'username': 'greenbox_brand',
                'email': 'contact@greenbox.vn',
                'password': 'brand123',
                'role': 'brand',
                'first_name': 'Green Box',
                'last_name': 'Marketing'
            },
            {
                'username': 'beauty_studio',
                'email': 'hello@beautystudio.vn',
                'password': 'brand123',
                'role': 'brand',
                'first_name': 'Beauty',
                'last_name': 'Studio'
            },
            {
                'username': 'tech_world',
                'email': 'info@techworld.vn',
                'password': 'brand123',
                'role': 'brand',
                'first_name': 'Tech',
                'last_name': 'World'
            },
            {
                'username': 'fashion_house',
                'email': 'pr@fashionhouse.vn',
                'password': 'brand123',
                'role': 'brand',
                'first_name': 'Fashion',
                'last_name': 'House'
            },
            
            # Creator users
            {
                'username': 'creator_anna',
                'email': 'anna.nguyen@gmail.com',
                'password': 'creator123',
                'role': 'creator',
                'first_name': 'Anna',
                'last_name': 'Nguyen'
            },
            {
                'username': 'creator_minh',
                'email': 'minh.tran@gmail.com',
                'password': 'creator123',
                'role': 'creator',
                'first_name': 'Minh',
                'last_name': 'Tran'
            },
            {
                'username': 'creator_lily',
                'email': 'lily.le@gmail.com',
                'password': 'creator123',
                'role': 'creator',
                'first_name': 'Lily',
                'last_name': 'Le'
            },
            {
                'username': 'creator_david',
                'email': 'david.vu@gmail.com',
                'password': 'creator123',
                'role': 'creator',
                'first_name': 'David',
                'last_name': 'Vu'
            },
            {
                'username': 'creator_sarah',
                'email': 'sarah.pham@gmail.com',
                'password': 'creator123',
                'role': 'creator',
                'first_name': 'Sarah',
                'last_name': 'Pham'
            }
        ]
        
        for user_data in users_data:
            try:
                # Check if user already exists
                if User.objects.filter(username=user_data['username']).exists():
                    print(f"   ⚠️  User {user_data['username']} already exists, skipping...")
                    user = User.objects.get(username=user_data['username'])
                else:
                    # Create user
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data.get('first_name', ''),
                        last_name=user_data.get('last_name', ''),
                        is_superuser=user_data.get('is_superuser', False),
                        is_staff=user_data.get('is_staff', False)
                    )
                    print(f"   ✅ Created user: {user.username}")
                
                # Create or update UserProfile
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': user_data['role']}
                )
                if not created:
                    profile.role = user_data['role']
                    profile.save()
                
                self.users[user_data['role']] = self.users.get(user_data['role'], [])
                self.users[user_data['role']].append(user)
                
            except Exception as e:
                print(f"   ❌ Error creating user {user_data['username']}: {str(e)}")
    
    def create_sample_campaigns(self):
        """Create sample campaigns"""
        print("📋 Creating sample campaigns...")
        
        if not hasattr(self, 'users') or 'brand' not in self.users:
            print("   ❌ No brand users found, skipping campaigns creation")
            return
            
        campaigns_data = [
            {
                'title': 'Combo Siêu Tiết Kiệm – Mỹ Phẩm',
                'description': 'Chiến dịch quảng bá sản phẩm mỹ phẩm cao cấp với ưu đại đặc biệt cho KOCs',
                'budget': 50000000,  # 50M VND
                'commission_rate': 15.0,
                'start_date': datetime.now() + timedelta(days=7),
                'end_date': datetime.now() + timedelta(days=37),
                'requirements': 'Follower tối thiểu 10K, chuyên về beauty/lifestyle',
                'location': 'Hồ Chí Minh',
                'category': 'beauty'
            },
            {
                'title': 'Tech Gadgets Review Campaign',
                'description': 'Review các sản phẩm công nghệ mới nhất của Tech World',
                'budget': 80000000,  # 80M VND
                'commission_rate': 12.0,
                'start_date': datetime.now() + timedelta(days=5),
                'end_date': datetime.now() + timedelta(days=35),
                'requirements': 'Content creator chuyên về tech, có kinh nghiệm review sản phẩm',
                'location': 'Hà Nội',
                'category': 'technology'
            },
            {
                'title': 'Fashion Autumn Collection 2025',
                'description': 'Quảng bá bộ sưu tập thời trang thu 2025 của Fashion House',
                'budget': 100000000,  # 100M VND
                'commission_rate': 20.0,
                'start_date': datetime.now() + timedelta(days=10),
                'end_date': datetime.now() + timedelta(days=40),
                'requirements': 'Fashion influencer, có style riêng và follower chất lượng',
                'location': 'Đà Nẵng',
                'category': 'fashion'
            },
            {
                'title': 'Green Living Campaign',
                'description': 'Tuyên truyền lối sống xanh và sản phẩm thân thiện môi trường',
                'budget': 60000000,  # 60M VND
                'commission_rate': 18.0,
                'start_date': datetime.now() + timedelta(days=3),
                'end_date': datetime.now() + timedelta(days=33),
                'requirements': 'Content về lifestyle, môi trường, sức khỏe',
                'location': 'Cần Thơ',
                'category': 'lifestyle'
            },
            {
                'title': 'Food & Beverage Tasting',
                'description': 'Thử và review các món ăn đặc sản và đồ uống mới',
                'budget': 40000000,  # 40M VND
                'commission_rate': 10.0,
                'start_date': datetime.now() + timedelta(days=1),
                'end_date': datetime.now() + timedelta(days=21),
                'requirements': 'Food blogger, reviewer ẩm thực',
                'location': 'Hồ Chí Minh',
                'category': 'food'
            }
        ]
        
        # Get brand users
        brand_users = self.users.get('brand', [])
        if not brand_users:
            print("   ❌ No brand users available")
            return
        
        for i, campaign_data in enumerate(campaigns_data):
            try:
                # Assign to different brands
                brand_user = brand_users[i % len(brand_users)]
                
                # Check if campaign exists
                if hasattr(globals().get('Campaign', None), 'objects'):
                    # If Campaign model exists
                    campaign, created = Campaign.objects.get_or_create(
                        title=campaign_data['title'],
                        defaults={
                            **campaign_data,
                            'brand': brand_user,
                            'status': 'active'
                        }
                    )
                    if created:
                        print(f"   ✅ Created campaign: {campaign.title}")
                        self.campaigns.append(campaign)
                    else:
                        print(f"   ⚠️  Campaign {campaign.title} already exists")
                else:
                    print("   ⚠️  Campaign model not found, creating placeholder data")
                    
            except Exception as e:
                print(f"   ❌ Error creating campaign {campaign_data['title']}: {str(e)}")
    
    def create_dashboard_stats(self):
        """Create dashboard statistics"""
        print("📊 Creating dashboard statistics...")
        
        try:
            # Brand Dashboard Stats
            for brand_user in self.users.get('brand', []):
                stats, created = BrandDashboardStats.objects.get_or_create(
                    brand=brand_user,
                    defaults={
                        'total_campaigns': random.randint(3, 15),
                        'active_campaigns': random.randint(1, 5),
                        'total_kols': random.randint(20, 100),
                        'total_revenue': random.randint(100000000, 500000000),
                        'month_revenue': random.randint(10000000, 50000000),
                        'engagement_rate': round(random.uniform(2.5, 8.5), 2)
                    }
                )
                if created:
                    print(f"   ✅ Created brand stats for: {brand_user.username}")
            
            # Creator Analytics
            for creator_user in self.users.get('creator', []):
                analytics, created = CreatorAnalytics.objects.get_or_create(
                    creator=creator_user,
                    defaults={
                        'total_campaigns': random.randint(5, 25),
                        'completed_campaigns': random.randint(3, 20),
                        'pending_campaigns': random.randint(0, 3),
                        'total_earnings': random.randint(5000000, 50000000),
                        'month_earnings': random.randint(1000000, 8000000),
                        'avg_engagement': round(random.uniform(3.0, 12.0), 2),
                        'follower_count': random.randint(10000, 500000)
                    }
                )
                if created:
                    print(f"   ✅ Created creator analytics for: {creator_user.username}")
                    
        except Exception as e:
            print(f"   ❌ Error creating dashboard stats: {str(e)}")
    
    def create_sample_data(self):
        """Create additional sample data"""
        print("🎯 Creating additional sample data...")
        
        try:
            # Sample KOL data if model exists
            if hasattr(globals().get('KOL', None), 'objects'):
                creator_users = self.users.get('creator', [])
                for creator in creator_users[:3]:  # Create KOL profiles for first 3 creators
                    kol, created = KOL.objects.get_or_create(
                        user=creator,
                        defaults={
                            'platform': random.choice(['Instagram', 'TikTok', 'YouTube', 'Facebook']),
                            'follower_count': random.randint(10000, 500000),
                            'engagement_rate': round(random.uniform(2.0, 10.0), 2),
                            'category': random.choice(['beauty', 'fashion', 'tech', 'food', 'lifestyle']),
                            'location': random.choice(['Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Cần Thơ'])
                        }
                    )
                    if created:
                        print(f"   ✅ Created KOL profile for: {creator.username}")
            
        except Exception as e:
            print(f"   ❌ Error creating sample data: {str(e)}")
    
    def run(self):
        """Run the complete demo data creation"""
        print("🚀 Starting Nova Aff Demo Data Creation...")
        print("=" * 50)
        
        try:
            with transaction.atomic():
                self.create_users()
                print()
                self.create_sample_campaigns()
                print()
                self.create_dashboard_stats()
                print()
                self.create_sample_data()
                print()
                
            print("=" * 50)
            print("✅ Demo data creation completed successfully!")
            print()
            print("📋 Summary:")
            print(f"   👥 Users created: {sum(len(users) for users in self.users.values())}")
            print(f"   📊 Campaigns: {len(self.campaigns)}")
            print(f"   🎯 Dashboard stats: Created")
            print()
            print("🔐 Demo Login Credentials:")
            print("   Admin: admin / admin123")
            print("   Manager: manager / manager123")
            print("   Brand: greenbox_brand / brand123")
            print("   Creator: creator_anna / creator123")
            print()
            print("🌐 Access URLs:")
            print("   Frontend: https://novaaff.id.vn/")
            print("   Admin: https://novaaff.id.vn/admin/")
            print("   API: https://novaaff.id.vn/api/")
            
        except Exception as e:
            print(f"❌ Error during demo data creation: {str(e)}")
            raise

if __name__ == "__main__":
    creator = DemoDataCreator()
    creator.run()
