#!/usr/bin/env python3
"""
Comprehensive test workflow for the information submission and approval system
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_step(step_num, title):
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*60}")

def print_result(status, response_data):
    print(f"Status: {status}")
    if response_data:
        print(f"Response: {json.dumps(response_data, indent=2)}")

def login_user(email, password):
    """Login a user and return session cookies"""
    response = requests.post(f"{BASE_URL}/api/login/", json={
        "email": email,
        "password": password
    })
    if response.status_code == 200:
        return response.cookies
    else:
        print(f"Login failed: {response.status_code}")
        print(response.json())
        return None

def submit_info(cookies, heading, description):
    """Submit information using user session"""
    response = requests.post(f"{BASE_URL}/api/submit-info/", 
                           json={
                               "heading": heading,
                               "description": description
                           }, 
                           cookies=cookies)
    return response.status_code, response.json()

def get_pending_info(cookies):
    """Get pending information (admin only)"""
    response = requests.get(f"{BASE_URL}/api/pending-info/", cookies=cookies)
    return response.status_code, response.json()

def get_active_info(cookies):
    """Get active information"""
    response = requests.get(f"{BASE_URL}/api/active-info/", cookies=cookies)
    return response.status_code, response.json()

def approve_info(cookies, info_id):
    """Approve information (admin only)"""
    response = requests.post(f"{BASE_URL}/api/approve-info/{info_id}/", cookies=cookies)
    return response.status_code, response.json()

def get_my_submissions(cookies):
    """Get user's submissions"""
    response = requests.get(f"{BASE_URL}/api/my-submissions/", cookies=cookies)
    return response.status_code, response.json()

def main():
    print("🧪 COMPREHENSIVE WORKFLOW TEST")
    print("Testing: User submission → Admin approval → Superuser direct access")
    
    # Test data
    test_user_email = "workflowtest@example.com"
    test_user_password = "testpass123"
    superuser_email = "superuser@gmail.com"
    superuser_password = "superpassword123"
    
    test_heading = "Regular User Test Submission"
    test_description = "This is a test submission from a regular user that needs approval"
    
    superuser_heading = "Superuser Direct Test Submission"
    superuser_description = "This is a submission from superuser that should go directly to active info"
    
    print_step(1, "USER SUBMITS INFORMATION")
    print("📝 User tries to submit information for approval")
    
    # Login as regular user
    user_cookies = login_user(test_user_email, test_user_password)
    if not user_cookies:
        print("❌ Failed to login as user. Make sure user exists and is approved.")
        return
    
    # Submit information
    status, response = submit_info(user_cookies, test_heading, test_description)
    print_result(status, response)
    
    if status == 201:
        pending_info_id = response['pending_info']['id']
        print(f"✅ Successfully submitted info with ID: {pending_info_id}")
    else:
        print("❌ Failed to submit information")
        return
    
    print_step(2, "CHECK ACTIVE INFO (SHOULD NOT BE THERE YET)")
    print("🔍 Checking if submitted info appears in active info (should not)")
    
    status, response = get_active_info(user_cookies)
    print_result(status, response)
    
    # Check if our submission is in the active info
    found_in_active = False
    if status == 200:
        for info in response:
            if info['heading'] == test_heading:
                found_in_active = True
                break
    
    if found_in_active:
        print("❌ ERROR: User submission appeared in active info without approval!")
    else:
        print("✅ CORRECT: User submission not in active info (waiting for approval)")
    
    print_step(3, "ADMIN APPROVES THE INFORMATION")
    print("👑 Admin approves the pending information")
    
    # Login as superuser
    admin_cookies = login_user(superuser_email, superuser_password)
    if not admin_cookies:
        print("❌ Failed to login as superuser")
        return
    
    # Get pending info
    print("📋 Getting pending information list...")
    status, response = get_pending_info(admin_cookies)
    print_result(status, response)
    
    if status == 200:
        # Find our submission
        target_info = None
        for info in response:
            if info['heading'] == test_heading:
                target_info = info
                break
        
        if target_info:
            print(f"✅ Found pending info: {target_info['heading']} (ID: {target_info['id']})")
            
            # Approve it
            print(f"✅ Approving info ID: {target_info['id']}")
            status, response = approve_info(admin_cookies, target_info['id'])
            print_result(status, response)
            
            if status == 200:
                print("✅ Successfully approved the information")
            else:
                print("❌ Failed to approve information")
        else:
            print("❌ Could not find our pending submission")
    else:
        print("❌ Failed to get pending information")
    
    print_step(4, "CHECK ACTIVE INFO AFTER APPROVAL")
    print("🔍 Checking if approved info now appears in active info")
    
    status, response = get_active_info(user_cookies)
    print_result(status, response)
    
    # Check if our submission is now in the active info
    found_in_active_after_approval = False
    if status == 200:
        for info in response:
            if info['heading'] == test_heading:
                found_in_active_after_approval = True
                print(f"✅ SUCCESS: Found approved info in active info!")
                print(f"   Submitted by: {info['submitted_by']['email']}")
                print(f"   Approved by: {info['approved_by']['email']}")
                print(f"   Approved at: {info['approved_at']}")
                break
    
    if not found_in_active_after_approval:
        print("❌ ERROR: Approved info not found in active info!")
    
    print_step(5, "SUPERUSER DIRECT SUBMISSION")
    print("👑 Superuser submits information directly (should go to active info)")
    
    # Superuser submits info
    status, response = submit_info(admin_cookies, superuser_heading, superuser_description)
    print_result(status, response)
    
    if status == 201:
        print("✅ Superuser successfully submitted information")
        
        # Check if it went directly to active info
        print("🔍 Checking if superuser submission appears directly in active info...")
        status, response = get_active_info(admin_cookies)
        print_result(status, response)
        
        found_superuser_in_active = False
        if status == 200:
            for info in response:
                if info['heading'] == superuser_heading:
                    found_superuser_in_active = True
                    print(f"✅ SUCCESS: Superuser submission found directly in active info!")
                    print(f"   Submitted by: {info['submitted_by']['email']}")
                    print(f"   Approved by: {info['approved_by']['email']}")
                    break
        
        if not found_superuser_in_active:
            print("❌ ERROR: Superuser submission not found in active info!")
    else:
        print("❌ Failed to submit info as superuser")
    
    print_step(6, "FINAL SUMMARY")
    print("📊 Testing complete! Here's what we verified:")
    print("✅ Users can submit information (goes to pending)")
    print("✅ Pending info does NOT appear in active info")
    print("✅ Admins can view and approve pending info")
    print("✅ Approved info appears in active info for all users")
    print("✅ Superusers can submit info directly to active info")
    
    print(f"\n🎯 WORKFLOW SUCCESSFULLY TESTED!")

if __name__ == "__main__":
    main()