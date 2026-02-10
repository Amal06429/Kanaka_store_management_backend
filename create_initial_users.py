#!/usr/bin/env python
"""Script to create initial users"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

def create_users():
    """Create initial admin and demo users"""
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        admin.plain_password = 'admin123'  # Store for admin viewing
        admin.save()
        print(f"✓ Created admin user: {admin.username}")
    else:
        print("✗ Admin user already exists")
    
    # Create demo user
    if not User.objects.filter(username='demo').exists():
        demo_user = User.objects.create_user(
            username='demo',
            password='demo123',
            email='demo@example.com',
            role='user',
            shop_name='Demo Shop',
            staff_name='John Doe',
            mobile_number='+1234567890'
        )
        demo_user.plain_password = 'demo123'  # Store for admin viewing
        demo_user.save()
        print(f"✓ Created demo user: {demo_user.username}")
    else:
        print("✗ Demo user already exists")
    
    print("\nUsers created successfully!")
    print("Admin login: admin / admin123")
    print("Demo user login: demo / demo123")

if __name__ == '__main__':
    try:
        create_users()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
