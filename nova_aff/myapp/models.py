from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
