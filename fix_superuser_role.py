"""
Script to update existing superusers to have role='admin'
Run this with: python manage.py shell < fix_superuser_role.py
Or in Django shell: python manage.py shell, then copy-paste the code
"""

from api.models import User

# Update all superusers to have role='admin'
superusers = User.objects.filter(is_superuser=True)
updated_count = 0

for user in superusers:
    if user.role != 'admin':
        user.role = 'admin'
        user.save()
        updated_count += 1
        print(f"Updated user '{user.username}' to admin role")

print(f"\nTotal superusers updated: {updated_count}")

# Also update staff users
staff_users = User.objects.filter(is_staff=True, is_superuser=False)
for user in staff_users:
    if user.role != 'admin':
        user.role = 'admin'
        user.save()
        updated_count += 1
        print(f"Updated staff user '{user.username}' to admin role")

print(f"Total users updated to admin role: {updated_count}")
