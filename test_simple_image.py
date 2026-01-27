#!/usr/bin/env python3
"""
Simple test to verify image upload is working with relative URLs
"""

import requests
import json
import os

BASE_URL = "http://localhost:8000"

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

def submit_info_with_image(cookies, heading, description, image_path=None):
    """Submit information with optional image"""
    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            files = {
                'heading': (None, heading),
                'description': (None, description),
                'image': (os.path.basename(image_path), img_file, 'image/png')
            }
            response = requests.post(f"{BASE_URL}/api/submit-info/", files=files, cookies=cookies)
    else:
        data = {
            "heading": heading,
            "description": description
        }
        response = requests.post(f"{BASE_URL}/api/submit-info/", json=data, cookies=cookies)
    
    return response.status_code, response.json()

def main():
    print("🔧 TESTING SIMPLE IMAGE UPLOAD")
    print("Testing: Image upload with relative URLs")
    
    # Test data
    superuser_email = "superuser@gmail.com"
    superuser_password = "superpassword123"
    
    test_heading = "Simple Image Test"
    test_description = "Testing simple image upload with relative URLs"
    image_path = "politics_backend/media/test_image.png"
    
    print("👑 Admin logs in to test image upload")
    
    admin_cookies = login_user(superuser_email, superuser_password)
    if not admin_cookies:
        print("❌ Failed to login as admin")
        return
    
    print("✅ Admin logged in successfully")
    
    print("📸 Admin uploads image with information")
    
    status, response = submit_info_with_image(admin_cookies, test_heading, test_description, image_path)
    print(f"Status: {status}")
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if status == 201:
        if 'active_info' in response and response['active_info'].get('image'):
            image_url = response['active_info']['image']
            print(f"✅ SUCCESS: Image URL returned: {image_url}")
            
            # Check if it's a relative URL (starts with /media/)
            if image_url.startswith('/media/'):
                print("✅ URL is relative (starts with /media/)")
                print("✅ This is the correct format!")
                
                # Test accessibility with full URL
                full_url = f"{BASE_URL}{image_url}"
                try:
                    image_response = requests.get(full_url)
                    if image_response.status_code == 200:
                        print("✅ Image is accessible!")
                        print(f"   Full URL: {full_url}")
                        print(f"   Content-Type: {image_response.headers.get('Content-Type', 'Unknown')}")
                        print(f"   Content-Length: {len(image_response.content)} bytes")
                    else:
                        print(f"❌ Image URL not accessible: {image_response.status_code}")
                except Exception as e:
                    print(f"❌ Error accessing image URL: {e}")
            else:
                print("❌ URL is not relative")
        else:
            print("❌ No image URL returned in response")
    else:
        print("❌ Failed to upload image with information")

if __name__ == "__main__":
    main()