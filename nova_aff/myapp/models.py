from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('brand', 'Brand'),
        ('creator', 'Creator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='creator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        ordering = ['-created_at']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)

class Project(models.Model):
    name = models.CharField(max_length=255)
    project_id = models.CharField(max_length=100, unique=True)
    created_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class KOL(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='kols')
    full_name = models.CharField(max_length=255)
    submitted_on = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    zalo = models.CharField(max_length=20)
    tiktok_url = models.URLField()
    tiktok_id = models.CharField(max_length=100)
    followers = models.CharField(max_length=20)
    gmv = models.CharField(max_length=20)
    channel_identifier = models.CharField(max_length=100)
    appropriate_channel_topic = models.CharField(max_length=255)
    shipping_address = models.TextField()
    brand_approval = models.CharField(max_length=100)
    note = models.TextField()
    kol_koc_approval_time = models.DateField()
    number_tracking = models.CharField(max_length=20)
    koc_confirmed_by_nova = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/kols/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at']


class DataTracking(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='data_tracking')
    creator = models.CharField(max_length=255)
    creator_id = models.CharField(max_length=100)
    about_video = models.CharField(max_length=255)
    video_id = models.CharField(max_length=100)
    upload_time = models.CharField(max_length=50)
    view = models.IntegerField()
    like = models.IntegerField()
    share = models.IntegerField()
    comment = models.IntegerField()
    product_linked = models.URLField()
    new_followers = models.IntegerField()
    product_impressions = models.IntegerField()
    product_entries = models.IntegerField()
    gmv = models.IntegerField()
    ctr = models.IntegerField()
    revenue_from_videos = models.IntegerField()
    video_file = models.FileField(upload_to='videos/data_tracking/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator} - {self.video_id}"

    class Meta:
        ordering = ['-created_at']


class TrackingNumber(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tracking_numbers')
    tracking_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    tracking_url = models.URLField()
    phone_check = models.BooleanField(default=False)
    tracking_date = models.DateField()
    tiktok_id = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/tracking/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking {self.tracking_number} - {self.phone_number}"

    class Meta:
        ordering = ['-created_at']


# Brand Analytics Models
class Creator(models.Model):
    CATEGORY_CHOICES = [
        ('beauty', 'Chăm sóc sắc đẹp'),
        ('baby', 'Trẻ sơ sinh'),
        ('health', 'Sức khỏe'),
        ('lifestyle', 'Lối sống'),
        ('fashion', 'Thời trang'),
        ('food', 'Ẩm thực'),
        ('tech', 'Công nghệ'),
        ('education', 'Giáo dục'),
        ('other', 'Khác'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ]
    
    # Basic info
    username = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=255)
    tiktok_url = models.URLField()
    avatar = models.URLField(null=True, blank=True)
    
    # Categories and demographics
    categories = models.JSONField(default=list)  # Store multiple categories
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    
    # Follower stats
    followers_count = models.BigIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.display_name} (@{self.username})"
    
    class Meta:
        ordering = ['-followers_count']


class BrandDashboardStats(models.Model):
    # Daily stats
    date = models.DateField(unique=True)
    clicks_today = models.IntegerField(default=0)
    orders_today = models.IntegerField(default=0)
    revenue_today = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stats for {self.date}"
    
    class Meta:
        ordering = ['-date']


class CreatorAnalytics(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='analytics')
    
    # Sales metrics
    gmv = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    products_sold = models.IntegerField(default=0)
    gpm = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    average_gmv_per_customer = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Commission data
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # percentage
    total_products = models.IntegerField(default=0)
    price_range_min = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_range_max = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    brands_collaborated = models.IntegerField(default=0)
    
    # Channel performance breakdown
    live_gmv_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    video_gmv_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    product_card_gmv_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Category performance breakdown (JSON field to store multiple categories with percentages)
    category_performance = models.JSONField(default=dict)
    
    # Date range for analytics
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.creator.display_name} Analytics ({self.start_date} - {self.end_date})"
    
    class Meta:
        ordering = ['-created_at']


class VideoAnalytics(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='video_analytics')
    
    # Video metrics
    total_videos = models.IntegerField(default=0)
    average_views = models.BigIntegerField(default=0)
    average_engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gpm_video = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Date range
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.creator.display_name} Video Analytics"
    
    class Meta:
        ordering = ['-created_at']


class LiveAnalytics(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='live_analytics')
    
    # Live stream metrics
    total_live_sessions = models.IntegerField(default=0)
    average_viewers = models.BigIntegerField(default=0)
    average_engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    gpm_live = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Date range
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.creator.display_name} Live Analytics"
    
    class Meta:
        ordering = ['-created_at']


class FollowerDemographics(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='follower_demographics')
    
    # Gender breakdown
    male_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    female_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Age breakdown
    age_18_24_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    age_25_34_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    age_35_44_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    age_45_54_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    age_55_plus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Top locations (JSON field to store location data)
    top_locations = models.JSONField(default=list)
    
    # Date snapshot
    snapshot_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.creator.display_name} Demographics ({self.snapshot_date})"
    
    class Meta:
        ordering = ['-snapshot_date']


class TrendData(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='trend_data')
    
    # Trend metrics over time
    date = models.DateField()
    gmv = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    products_sold = models.IntegerField(default=0)
    followers_gained = models.IntegerField(default=0)
    video_views = models.BigIntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.creator.display_name} - {self.date}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ['creator', 'date']