#!/usr/bin/env python3
"""
Script to check the PendingInfo and ActiveInfo tables
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'politics_backend.settings')
sys.path.append('/Users/manibharadwaj/Developer/compnay/cloned/politics/politics_backend/politics_backend')
django.setup()

from users.models import PendingInfo, ActiveInfo

def check_info_tables():
    print("📊 CHECKING INFORMATION TABLES")
    print("=" * 50)
    
    # Check PendingInfo
    print("\n1️⃣  PendingInfo Table:")
    pending_info = PendingInfo.objects.all()
    for info in pending_info:
        print(f"   • ID: {info.id}")
        print(f"     Heading: {info.heading}")
        print(f"     Submitted by: {info.submitted_by.email}")
        print(f"     Status: {info.status}")
        print(f"     Submitted at: {info.submitted_at}")
        print()
    
    # Check ActiveInfo
    print("\n2️⃣  ActiveInfo Table:")
    active_info = ActiveInfo.objects.all()
    for info in active_info:
        print(f"   • ID: {info.id}")
        print(f"     Heading: {info.heading}")
        print(f"     Submitted by: {info.submitted_by.email}")
        print(f"     Approved by: {info.approved_by.email}")
        print(f"     Approved at: {info.approved_at}")
        print(f"     Created at: {info.created_at}")
        print()
    
    print(f"📊 SUMMARY:")
    print(f"   Pending Info: {pending_info.count()}")
    print(f"   Active Info: {active_info.count()}")

if __name__ == "__main__":
    check_info_tables()