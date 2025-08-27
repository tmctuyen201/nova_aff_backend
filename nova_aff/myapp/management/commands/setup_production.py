from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup production environment for Nova Aff'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser account',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@novaaff.id.vn',
            help='Superuser email address',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Setting up Nova Aff production environment...')
        )

        try:
            with transaction.atomic():
                # Create superuser if requested
                if options['create_superuser']:
                    self.create_superuser(options['email'])

                # Setup basic data
                self.setup_basic_data()

                self.stdout.write(
                    self.style.SUCCESS('✅ Production setup completed successfully!')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Setup failed: {str(e)}')
            )
            raise

    def create_superuser(self, email):
        """Create superuser if it doesn't exist"""
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email=email,
                password=os.getenv('ADMIN_PASSWORD', 'admin123')
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superuser created: {user.username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Superuser already exists')
            )

    def setup_basic_data(self):
        """Setup basic application data"""
        # Add any initial data setup here
        # For example: default categories, settings, etc.
        self.stdout.write('Setting up basic application data...')
        
        # Example: Create default categories
        # from myapp.models import Category
        # Category.objects.get_or_create(name='Technology', defaults={'description': 'Tech products'})
        
        self.stdout.write('✅ Basic data setup completed')
