#!/usr/bin/env python
"""Test the API endpoint directly"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from api.views import UploadedFileViewSet

User = get_user_model()

def test_files_endpoint():
    """Test the files endpoint with admin user"""
    print("=" * 60)
    print("TESTING FILES API ENDPOINT")
    print("=" * 60)
    
    # Get admin user
    admin = User.objects.filter(role='admin').first()
    if not admin:
        print("ERROR: No admin user found")
        return
    
    print(f"\nTesting with user: {admin.username} (role: {admin.role})")
    
    # Create request
    factory = APIRequestFactory()
    request = factory.get('/api/files/')
    force_authenticate(request, user=admin)
    
    # Get viewset response
    view = UploadedFileViewSet.as_view({'get': 'list'})
    response = view(request)
    
    print(f"\nResponse status: {response.status_code}")
    print(f"Response data: {response.data}")
    
    if hasattr(response, 'data'):
        if isinstance(response.data, dict) and 'results' in response.data:
            print(f"\nFiles returned: {len(response.data['results'])}")
            for file in response.data['results']:
                print(f"  - {file.get('name', 'N/A')} by {file.get('user_name', 'N/A')}")
        elif isinstance(response.data, list):
            print(f"\nFiles returned: {len(response.data)}")
            for file in response.data:
                print(f"  - {file.get('name', 'N/A')} by {file.get('user_name', 'N/A')}")
    
    print("=" * 60)

if __name__ == '__main__':
    test_files_endpoint()
