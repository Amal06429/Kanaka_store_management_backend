from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = 'Fix superuser roles - set role to admin for all superusers and staff'

    def handle(self, *args, **options):
        # Update all superusers to have role='admin'
        superusers = User.objects.filter(is_superuser=True)
        updated_count = 0

        self.stdout.write("Fixing superuser roles...\n")

        for user in superusers:
            if user.role != 'admin':
                user.role = 'admin'
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Updated user '{user.username}' to admin role")
                )
            else:
                self.stdout.write(f"  User '{user.username}' already has admin role")

        # Also update staff users
        staff_users = User.objects.filter(is_staff=True, is_superuser=False)
        for user in staff_users:
            if user.role != 'admin':
                user.role = 'admin'
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Updated staff user '{user.username}' to admin role")
                )

        self.stdout.write("\n" + "="*50)
        self.stdout.write(
            self.style.SUCCESS(f"✓ Total users updated to admin role: {updated_count}")
        )
        self.stdout.write(
            f"  Total superusers: {superusers.count()}"
        )
        self.stdout.write("="*50 + "\n")
