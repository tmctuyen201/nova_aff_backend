#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova_aff.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Create an admin user for testing"""
    try:
        # Check if admin user already exists
        if User.objects.filter(username='admin').exists():
            print("Admin user already exists!")
            admin_user = User.objects.get(username='admin')
        else:
            # Create admin user
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@nova-aff.com',
                password='admin123',
                is_staff=True,
                is_superuser=True
            )
            print("Admin user created successfully!")
        
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Is Staff: {admin_user.is_staff}")
        print(f"Is Superuser: {admin_user.is_superuser}")
        print("\nYou can now login with:")
        print("Username: admin")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin_user() 