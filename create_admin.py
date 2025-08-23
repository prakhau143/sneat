#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sneat_project.settings')
django.setup()

from django.contrib.auth.models import User

# Check if admin user already exists
if User.objects.filter(username='admin').exists():
    print("Admin user already exists. Updating password...")
    user = User.objects.get(username='admin')
    user.set_password('admin')
    user.save()
    print("Admin user password updated to 'admin'")
else:
    # Create new admin user
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin'
    )
    print("Admin superuser created successfully!")
    print("Username: admin")
    print("Password: admin")
    print("Email: admin@example.com")

print("\nYou can now login at: http://127.0.0.1:8000/")
print("Super Admin Dashboard: http://127.0.0.1:8000/super-admin/dashboard/")
print("Settings Profile: http://127.0.0.1:8000/super-admin/settings/profile/")
