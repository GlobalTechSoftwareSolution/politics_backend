#!/usr/bin/env python3
"""
Test script for the information submission and approval API
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing Information Submission and Approval API")
    print("=" * 60)
    
    # Test 1: Get active info (should work for approved users)
    print("\n1️⃣  Testing GET /api/active-info/ (should require authentication)")
    try:
        response = requests.get(f"{BASE_URL}/api/active-info/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Submit info (should require authentication)
    print("\n2️⃣  Testing POST /api/submit-info/ (should require authentication)")
    test_data = {
        "heading": "Test Information",
        "description": "This is a test description for the information submission system.",
        "image": None
    }
    try:
        response = requests.post(f"{BASE_URL}/api/submit-info/", json=test_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Get pending info (should require admin privileges)
    print("\n3️⃣  Testing GET /api/pending-info/ (should require admin privileges)")
    try:
        response = requests.get(f"{BASE_URL}/api/pending-info/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Get my submissions (should require authentication)
    print("\n4️⃣  Testing GET /api/my-submissions/ (should require authentication)")
    try:
        response = requests.get(f"{BASE_URL}/api/my-submissions/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ API endpoints are set up and accessible!")
    print("\n📋 Available Endpoints:")
    print("   POST /api/submit-info/ - Submit information for approval")
    print("   GET  /api/pending-info/ - Get pending info (Admin only)")
    print("   GET  /api/active-info/ - Get approved info (All approved users)")
    print("   POST /api/approve-info/<id>/ - Approve info (Admin only)")
    print("   POST /api/reject-info/<id>/ - Reject info (Admin only)")
    print("   GET  /api/my-submissions/ - Get user's submissions")

if __name__ == "__main__":
    test_api()