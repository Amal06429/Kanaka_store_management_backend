#!/usr/bin/env python
"""Script to check uploaded files in the database"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import UploadedFile, User

def check_files():
    """Check all files in the database"""
    print("=" * 60)
    print("UPLOADED FILES IN DATABASE")
    print("=" * 60)
    
    total_files = UploadedFile.objects.count()
    print(f"\nTotal files in database: {total_files}")
    
    if total_files > 0:
        print("\nFiles:")
        for file in UploadedFile.objects.all():
            print(f"  - ID: {file.id}")
            print(f"    Name: {file.name}")
            print(f"    User: {file.user.username} (ID: {file.user.id})")
            print(f"    Heading: {file.heading}")
            print(f"    Type: {file.file_type}")
            print(f"    Size: {file.get_file_size_display()}")
            print(f"    Uploaded: {file.uploaded_at}")
            print(f"    File path: {file.file}")
            print()
    else:
        print("\n  No files uploaded yet.")
    
    print("\nUsers in database:")
    for user in User.objects.all():
        file_count = UploadedFile.objects.filter(user=user).count()
        print(f"  - {user.username} ({user.role}): {file_count} files")
    
    print("=" * 60)

if __name__ == '__main__':
    try:
        check_files()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
