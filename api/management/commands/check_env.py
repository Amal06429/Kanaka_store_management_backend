"""
Environment Variables Check Script for File Upload
Run this on your hosted server to check if all required environment variables are set:
python manage.py check_env
"""

from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Check if all required environment variables are set for file uploads'

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*60)
        self.stdout.write("ENVIRONMENT VARIABLES CHECK")
        self.stdout.write("="*60 + "\n")

        # Required environment variables
        env_vars = {
            'CLOUDFLARE_R2_ENABLED': 'Controls if R2 storage is enabled',
            'CLOUDFLARE_R2_ACCESS_KEY': 'R2 Access Key',
            'CLOUDFLARE_R2_SECRET_KEY': 'R2 Secret Key',
            'CLOUDFLARE_R2_BUCKET': 'R2 Bucket Name',
            'CLOUDFLARE_R2_ACCOUNT_ID': 'R2 Account ID',
        }

        all_set = True

        for var_name, description in env_vars.items():
            value = os.getenv(var_name)
            if value:
                # Show only first and last 4 chars for security
                if 'KEY' in var_name or 'SECRET' in var_name:
                    display_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
                else:
                    display_value = value
                    
                self.stdout.write(
                    self.style.SUCCESS(f"✓ {var_name}: {display_value}")
                )
                self.stdout.write(f"  ({description})\n")
            else:
                all_set = False
                self.stdout.write(
                    self.style.ERROR(f"✗ {var_name}: NOT SET")
                )
                self.stdout.write(f"  ({description})\n")

        self.stdout.write("="*60)
        
        if all_set:
            self.stdout.write(
                self.style.SUCCESS("\n✓ All environment variables are set!\n")
            )
            
            # Check if R2 is enabled
            if os.getenv("CLOUDFLARE_R2_ENABLED", "False") == "True":
                self.stdout.write(
                    self.style.SUCCESS("✓ Cloudflare R2 storage is ENABLED\n")
                )
            else:
                self.stdout.write(
                    self.style.WARNING("⚠ Cloudflare R2 storage is DISABLED\n")
                )
                self.stdout.write("  Files will be saved locally instead of R2\n")
        else:
            self.stdout.write(
                self.style.ERROR("\n✗ Some environment variables are missing!\n")
            )
            self.stdout.write("  Add them to your .env file or server environment\n")

        self.stdout.write("="*60 + "\n")
