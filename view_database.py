#!/usr/bin/env python3
"""
Script to view database contents
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'politics_backend.settings')
sys.path.append('/Users/manibharadwaj/Developer/compnay/cloned/politics/politics_backend/politics_backend')
django.setup()

from users.models import User
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token

def view_database():
    print("🗄️  DATABASE CONTENTS")
    print("=" * 50)
    
    # View custom users
    print("\n1️⃣  Custom Users (users_user table):")
    users = User.objects.all()
    for user in users:
        print(f"   • ID: {user.id}")
        print(f"     Email: {user.email}")
        print(f"     Approved: {user.is_approved}")
        print(f"     User: {user.is_user}")
        print(f"     Superuser: {user.is_superuser}")
        print(f"     Created: {user.created_at}")
        if user.approval_date:
            print(f"     Approved: {user.approval_date}")
        print()
    
    # View tokens
    print("\n2️⃣  API Tokens (authtoken_token table):")
    tokens = Token.objects.all()
    for token in tokens:
        print(f"   • Token: {token.key[:10]}...")
        print(f"     User: {token.user.email}")
        print()
    
    # View pending users
    print("\n3️⃣  Pending Users (Not Approved):")
    pending_users = User.objects.filter(is_approved=False)
    for user in pending_users:
        print(f"   • {user.email} (ID: {user.id})")
    
    # View approved users
    print("\n4️⃣  Approved Users:")
    approved_users = User.objects.filter(is_approved=True)
    for user in approved_users:
        print(f"   • {user.email} (User: {user.is_user})")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total Users: {User.objects.count()}")
    print(f"   Pending Users: {pending_users.count()}")
    print(f"   Approved Users: {approved_users.count()}")
    print(f"   User Role Users: {User.objects.filter(is_user=True).count()}")
    print(f"   Superusers: {User.objects.filter(is_superuser=True).count()}")
    print(f"   Active Tokens: {Token.objects.count()}")

if __name__ == "__main__":
    view_database()
    