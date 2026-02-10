#!/usr/bin/env python
"""Script to reset migrations for custom user model"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

def reset_migrations():
    """Clear migration history and rebuild"""
    with connection.cursor() as cursor:
        # Delete all migration records
        cursor.execute("DELETE FROM django_migrations;")
        print("✓ Cleared migration history")
        
        # Drop all tables
        cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        print("✓ Dropped all tables")
    
    print("\nNow run:")
    print("  python manage.py migrate")

if __name__ == '__main__':
    try:
        reset_migrations()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
