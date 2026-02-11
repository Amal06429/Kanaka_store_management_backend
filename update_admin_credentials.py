#!/usr/bin/env python
"""Script to update admin credentials"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

def update_admin_credentials():
    """Update admin username and password"""
    try:
        # Find existing admin user
        admin = User.objects.get(username='adminkanaka@gmail.com')
        
        # Update credentials
        new_username = 'fayis@kanaka.com'
        new_password = 'admin@fayiskanaka'
        
        admin.username = new_username
        admin.email = new_username
        admin.set_password(new_password)
        admin.plain_password = new_password  # Store for admin viewing
        admin.save()
        
        print(f"✓ Admin credentials updated successfully!")
        print(f"New username: {new_username}")
        print(f"New password: {new_password}")
        
    except User.DoesNotExist:
        print("✗ Admin user 'adminkanaka@gmail.com' not found")
        print("Creating new admin user...")
        
        # Create new admin user
        admin = User.objects.create_user(
            username='fayis@kanaka.com',
            password='admin@fayiskanaka',
            email='fayis@kanaka.com',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        admin.plain_password = 'admin@fayiskanaka'
        admin.save()
        print(f"✓ Created new admin user: {admin.username}")

if __name__ == '__main__':
    try:
        update_admin_credentials()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
