#!/usr/bin/env python3
"""
Script to create a regular test user for workflow testing
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'politics_backend.settings')
sys.path.append('/Users/manibharadwaj/Developer/compnay/cloned/politics/politics_backend/politics_backend')
django.setup()

from users.models import User

def create_test_user():
    print("👤 Creating test user for workflow testing...")
    
    # Create a regular user (not admin)
    try:
        test_user = User.objects.create_user(
            email='workflowtest@example.com',
            password='testpass123',
            fullname='Workflow Test User'
        )
        
        # Approve the user but don't make them admin
        test_user.is_approved = True
        test_user.approval_date = timezone.now()
        test_user.save()
        
        print(f"✅ Created test user: {test_user.email}")
        print(f"   ID: {test_user.id}")
        print(f"   Approved: {test_user.is_approved}")
        print(f"   User role: {test_user.is_user}")
        print(f"   Superuser: {test_user.is_superuser}")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")

if __name__ == "__main__":
    from django.utils import timezone
    create_test_user()