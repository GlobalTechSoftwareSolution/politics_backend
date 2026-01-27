#!/usr/bin/env python3
"""
Script to reset superuser password
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'politics_backend.settings')
sys.path.append('/Users/manibharadwaj/Developer/compnay/cloned/politics/politics_backend/politics_backend')
django.setup()

from users.models import User

def reset_superuser_password():
    print("🔑 Resetting superuser password...")
    
    try:
        superuser = User.objects.get(email='superuser@gmail.com')
        superuser.set_password('superpassword123')
        superuser.save()
        print(f"✅ Reset password for {superuser.email}")
        print(f"   New password: superpassword123")
        
    except User.DoesNotExist:
        print("❌ Superuser not found")

if __name__ == "__main__":
    reset_superuser_password()