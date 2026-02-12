"""
Simple script to update superuser roles
Run this by:
1. python manage.py shell
2. Copy and paste the code below
"""

from api.models import User

# Update all superusers to have role='admin'
superusers = User.objects.filter(is_superuser=True)
for user in superusers:
    user.role = 'admin'
    user.save()
    print(f"✓ Updated {user.username} to admin role")

print(f"\n✓ Done! Updated {superusers.count()} superuser(s)")
