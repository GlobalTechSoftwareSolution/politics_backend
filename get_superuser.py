#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'politics_backend.politics_backend.settings')
django.setup()

from users.models import User

print("🔍 Finding superuser credentials...")
print("=" * 50)

superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    for user in superusers:
        print(f"📧 Superuser Email: {user.email}")
        print(f"👤 Full Name: {user.fullname}")
        print(f"✅ Is Active: {user.is_approved}")
        print(f"🆔 User ID: {user.id}")
        print(f"📅 Created: {user.created_at}")
        print("-" * 30)
else:
    print("❌ No superusers found in the database")

print("\n💡 Note: To get the password, you'll need to reset it using:")
print("   python manage.py shell")
print("   from django.contrib.auth import get_user_model")
print("   User = get_user_model()")
print("   user = User.objects.get(email='superuser@gmail.com')")
print("   user.set_password('new_password')")
print("   user.save()")