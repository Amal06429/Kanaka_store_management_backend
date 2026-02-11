#!/usr/bin/env python
"""Script to update existing users with plain passwords for admin viewing"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import User

def update_passwords():
    """Update plain_password field for existing users"""
    # Update admin user
    try:
        admin = User.objects.get(username='fayis@kanaka.com')
        admin.plain_password = 'admin@fayiskanaka'
        admin.save()
        print(f"✓ Updated admin user password field")
    except User.DoesNotExist:
        print("✗ Admin user not found")
    
    # Update demo user
    try:
        demo = User.objects.get(username='demo')
        demo.plain_password = 'demo123'
        demo.save()
        print(f"✓ Updated demo user password field")
    except User.DoesNotExist:
        print("✗ Demo user not found")
    
    print("\nUser passwords updated successfully!")
    print("Note: Only newly created or updated users will have viewable passwords.")

if __name__ == '__main__':
    try:
        update_passwords()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
