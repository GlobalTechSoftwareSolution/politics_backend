# Information Submission and Approval API - Postman Collection

This document provides all the curl commands and Postman collection details for testing the information submission and approval system.

## Base URL
```
http://localhost:8000
```

## Authentication

The API uses session-based authentication. You need to:
1. Login first to get session cookies
2. Use those cookies in subsequent requests

## 1. User Registration

### POST /api/register/
Register a new user account

**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "fullname": "New User"
  }'
```

**Response:**
```json
{
  "message": "User registered successfully. Please wait for approval.",
  "user": {
    "id": 34,
    "email": "newuser@example.com",
    "fullname": "New User",
    "role": "user",
    "is_approved": false,
    "is_user": false,
    "is_superuser": false,
    "created_at": "2026-01-27T11:35:00.000000Z",
    "approval_date": null
  }
}
```

## 2. User Login

### POST /api/login/
Login and get session cookies

**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "workflowtest@example.com",
    "password": "testpass123"
  }' \
  -c cookies.txt
```

**Response:**
```json
{
  "message": "Login successful",
  "user": {
    "id": 33,
    "email": "workflowtest@example.com",
    "fullname": "Workflow Test User",
    "role": "user",
    "is_approved": true,
    "is_user": false,
    "is_superuser": false,
    "created_at": "2026-01-27T11:27:05.554039Z",
    "approval_date": "2026-01-27T11:27:05.560869Z"
  },
  "note": "Session-based authentication - no JWT tokens"
}
```

## 3. User Profile

### GET /api/profile/
Get current user profile

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/profile/ \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "User profile retrieved successfully",
  "user": {
    "id": 33,
    "email": "workflowtest@example.com",
    "fullname": "Workflow Test User",
    "role": "user",
    "is_approved": true,
    "is_user": false,
    "is_superuser": false,
    "created_at": "2026-01-27T11:27:05.554039Z",
    "approval_date": "2026-01-27T11:27:05.560869Z"
  },
  "note": "Session-based authentication working"
}
```

## 4. Submit Information

### POST /api/submit-info/
Submit information for approval

**For Regular Users (goes to pending):**
```bash
curl -X POST http://localhost:8000/api/submit-info/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "heading": "My Test Information",
    "description": "This is a test description for the information submission system.",
    "image": null
  }'
```

**For Admin/Super Users (goes directly to active):**
```bash
curl -X POST http://localhost:8000/api/submit-info/ \
  -H "Content-Type: application/json" \
  -b admin_cookies.txt \
  -d '{
    "heading": "Admin Direct Submission",
    "description": "This is a direct submission from admin.",
    "image": null
  }'
```

### POST /api/submit-info/ (WITH IMAGE UPLOAD)
Upload local image file with information

**Upload Image with Information:**
```bash
curl -X POST http://localhost:8000/api/submit-info/ \
  -F "heading=Information with Image" \
  -F "description=This information includes an uploaded image" \
  -F "image=@/path/to/your/image.jpg" \
  -b cookies.txt
```

**Response with Absolute Image URL:**
```json
{
  "message": "Information submitted successfully for approval",
  "pending_info": {
    "id": 1,
    "heading": "Information with Image",
    "description": "This information includes an uploaded image",
    "image": "http://localhost:8000/media/info_images/image.jpg",
    "submitted_by": {
      "id": 33,
      "email": "workflowtest@example.com",
      "fullname": "Workflow Test User",
      "role": "user",
      "is_approved": true,
      "is_user": false,
      "is_superuser": false,
      "created_at": "2026-01-27T11:27:05.554039Z",
      "approval_date": "2026-01-27T11:27:05.560869Z"
    },
    "submitted_at": "2026-01-27T11:40:00.000000Z",
    "status": "pending"
  }
}
```

**Absolute Image URL (Copy from Database):**
```bash
# The absolute URL returned can be copied directly from database:
curl http://localhost:8000/media/info_images/image.jpg

# Or viewed in browser:
# http://localhost:8000/media/info_images/image.jpg

# ✅ This URL can be copied from database and pasted anywhere!
# ✅ Works in any browser, app, or platform
# ✅ No need to construct URLs manually
```

**Frontend Image Display with Absolute URL:**
```html
<img src="http://localhost:8000/media/info_images/image.jpg" alt="Uploaded Image" />
```

**Mobile App Integration:**
```swift
// iOS Swift - Direct URL usage
let imageUrl = URL(string: "http://localhost:8000/media/info_images/image.jpg")!
imageView.loadImage(from: imageUrl)
```

```kotlin
// Android Kotlin - Direct URL usage
val imageUrl = "http://localhost:8000/media/info_images/image.jpg"
Glide.with(context).load(imageUrl).into(imageView)
```

**Frontend Image Display:**
```html
<img src="http://localhost:8000/media/info_images/image.jpg" alt="Uploaded Image" />
```

**Response for Regular User:**
```json
{
  "message": "Information submitted successfully for approval",
  "pending_info": {
    "id": 1,
    "heading": "My Test Information",
    "description": "This is a test description for the information submission system.",
    "image": null,
    "submitted_by": {
      "id": 33,
      "email": "workflowtest@example.com",
      "fullname": "Workflow Test User",
      "role": "user",
      "is_approved": true,
      "is_user": false,
      "is_superuser": false,
      "created_at": "2026-01-27T11:27:05.554039Z",
      "approval_date": "2026-01-27T11:27:05.560869Z"
    },
    "submitted_at": "2026-01-27T11:40:00.000000Z",
    "status": "pending"
  }
}
```

**Response for Admin User:**
```json
{
  "message": "Information submitted and approved directly (admin privilege)",
  "active_info": {
    "id": 1,
    "heading": "Admin Direct Submission",
    "description": "This is a direct submission from admin.",
    "image": null,
    "submitted_by": {
      "id": 1,
      "email": "superuser@gmail.com",
      "fullname": "",
      "role": "user",
      "is_approved": true,
      "is_user": true,
      "is_superuser": true,
      "created_at": "2026-01-27T05:26:30.180846Z",
      "approval_date": "2026-01-27T10:49:47.098271Z"
    },
    "approved_by": {
      "id": 1,
      "email": "superuser@gmail.com",
      "fullname": "",
      "role": "user",
      "is_approved": true,
      "is_user": true,
      "is_superuser": true,
      "created_at": "2026-01-27T05:26:30.180846Z",
      "approval_date": "2026-01-27T10:49:47.098271Z"
    },
    "approved_at": "2026-01-27T11:40:00.000000Z",
    "created_at": "2026-01-27T11:40:00.000000Z"
  }
}
```

## 5. Get Active Information

### GET /api/active-info/
Get all approved information

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/active-info/ \
  -b cookies.txt
```

**Response:**
```json
[
  {
    "id": 1,
    "heading": "Admin Direct Submission",
    "description": "This is a direct submission from admin.",
    "image": null,
    "submitted_by": {
      "id": 1,
      "email": "superuser@gmail.com",
      "fullname": "",
      "role": "user",
      "is_approved": true,
      "is_user": true,
      "is_superuser": true,
      "created_at": "2026-01-27T05:26:30.180846Z",
      "approval_date": "2026-01-27T10:49:47.098271Z"
    },
    "approved_by": {
      "id": 1,
      "email": "superuser@gmail.com",
      "fullname": "",
      "role": "user",
      "is_approved": true,
      "is_user": true,
      "is_superuser": true,
      "created_at": "2026-01-27T05:26:30.180846Z",
      "approval_date": "2026-01-27T10:49:47.098271Z"
    },
    "approved_at": "2026-01-27T11:40:00.000000Z",
    "created_at": "2026-01-27T11:40:00.000000Z"
  }
]
```

## 6. Get Pending Information (Admin Only)

### GET /api/pending-info/
Get all pending information that needs approval

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/pending-info/ \
  -b admin_cookies.txt
```

**Response:**
```json
[
  {
    "id": 1,
    "heading": "My Test Information",
    "description": "This is a test description for the information submission system.",
    "image": null,
    "submitted_by": {
      "id": 33,
      "email": "workflowtest@example.com",
      "fullname": "Workflow Test User",
      "role": "user",
      "is_approved": true,
      "is_user": false,
      "is_superuser": false,
      "created_at": "2026-01-27T11:27:05.554039Z",
      "approval_date": "2026-01-27T11:27:05.560869Z"
    },
    "submitted_at": "2026-01-27T11:40:00.000000Z",
    "status": "pending"
  }
]
```

## 7. Approve Information (Admin Only)

### POST /api/approve-info/{id}/
Approve a pending information submission

**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/approve-info/1/ \
  -b admin_cookies.txt
```

**Response:**
```json
{
  "message": "Information approved successfully",
  "pending_info": {
    "id": 1,
    "heading": "My Test Information",
    "description": "This is a test description for the information submission system.",
    "image": null,
    "submitted_by": {
      "id": 33,
      "email": "workflowtest@example.com",
      "fullname": "Workflow Test User",
      "role": "user",
      "is_approved": true,
      "is_user": false,
      "is_superuser": false,
      "created_at": "2026-01-27T11:27:05.554039Z",
      "approval_date": "2026-01-27T11:27:05.560869Z"
    },
    "submitted_at": "2026-01-27T11:40:00.000000Z",
    "status": "approved"
  }
}
```

## 8. Reject Information (Admin Only)

### POST /api/reject-info/{id}/
Reject a pending information submission

**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/reject-info/1/ \
  -b admin_cookies.txt
```

**Response:**
```json
{
  "message": "Information rejected successfully",
  "pending_info": {
    "id": 1,
    "heading": "My Test Information",
    "description": "This is a test description for the information submission system.",
    "image": null,
    "submitted_by": {
      "id": 33,
      "email": "workflowtest@example.com",
      "fullname": "Workflow Test User",
      "role": "user",
      "is_approved": true,
      "is_user": false,
      "is_superuser": false,
      "created_at": "2026-01-27T11:27:05.554039Z",
      "approval_date": "2026-01-27T11:27:05.560869Z"
    },
    "submitted_at": "2026-01-27T11:40:00.000000Z",
    "status": "rejected"
  }
}
```

## 9. Get User's Submissions

### GET /api/my-submissions/
Get current user's pending and approved submissions

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/my-submissions/ \
  -b cookies.txt
```

**Response:**
```json
{
  "pending_submissions": [
    {
      "id": 1,
      "heading": "My Test Information",
      "description": "This is a test description for the information submission system.",
      "image": null,
      "submitted_by": {
        "id": 33,
        "email": "workflowtest@example.com",
        "fullname": "Workflow Test User",
        "role": "user",
        "is_approved": true,
        "is_user": false,
        "is_superuser": false,
        "created_at": "2026-01-27T11:27:05.554039Z",
        "approval_date": "2026-01-27T11:27:05.560869Z"
      },
      "submitted_at": "2026-01-27T11:40:00.000000Z",
      "status": "pending"
    }
  ],
  "approved_submissions": [
    {
      "id": 2,
      "heading": "Another Approved Info",
      "description": "This is another approved information.",
      "image": null,
      "submitted_by": {
        "id": 33,
        "email": "workflowtest@example.com",
        "fullname": "Workflow Test User",
        "role": "user",
        "is_approved": true,
        "is_user": false,
        "is_superuser": false,
        "created_at": "2026-01-27T11:27:05.554039Z",
        "approval_date": "2026-01-27T11:27:05.560869Z"
      },
      "approved_by": {
        "id": 1,
        "email": "superuser@gmail.com",
        "fullname": "",
        "role": "user",
        "is_approved": true,
        "is_user": true,
        "is_superuser": true,
        "created_at": "2026-01-27T05:26:30.180846Z",
        "approval_date": "2026-01-27T10:49:47.098271Z"
      },
      "approved_at": "2026-01-27T11:45:00.000000Z",
      "created_at": "2026-01-27T11:45:00.000000Z"
    }
  ]
}
```

## 10. Admin Endpoints

### GET /api/pending-users/ (Admin Only)
Get list of users waiting for approval

**Curl Command:**
```bash
curl -X GET http://localhost:8000/api/pending-users/ \
  -b admin_cookies.txt
```

### POST /api/approve-user/{user_id}/ (Admin Only)
Approve a user

**Curl Command:**
```bash
curl -X POST http://localhost:8000/api/approve-user/34/ \
  -b admin_cookies.txt
```

## Postman Collection Setup

### 1. Create Environment Variables
```
BASE_URL: http://localhost:8000
USER_EMAIL: workflowtest@example.com
USER_PASSWORD: testpass123
ADMIN_EMAIL: superuser@gmail.com
ADMIN_PASSWORD: superpassword123
```

### 2. Create Collection with Folders:
- **Authentication**
  - Register User
  - Login User
  - Get Profile

- **Information Management**
  - Submit Information (User)
  - Submit Information (Admin)
  - Get Active Info
  - Get Pending Info (Admin)
  - Approve Info (Admin)
  - Reject Info (Admin)
  - Get My Submissions

- **Admin Management**
  - Get Pending Users
  - Approve User

### 3. Pre-request Scripts for Authentication
Add this to requests that require authentication:
```javascript
// Check if we have session cookies
if (!pm.cookies.has('sessionid')) {
    // Login first
    pm.sendRequest({
        url: pm.environment.get("BASE_URL") + "/api/login/",
        method: 'POST',
        header: 'Content-Type: application/json',
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                email: pm.environment.get("USER_EMAIL"),
                password: pm.environment.get("USER_PASSWORD")
            })
        }
    }, function (err, response) {
        if (err) {
            console.log(err);
        }
    });
}
```

## Testing Workflow

### Complete User Workflow:
1. Register new user
2. Login as user
3. Submit information (goes to pending)
4. Login as admin
5. View pending information
6. Approve information
7. Login as user again
8. View active information (should see approved info)

### Admin Direct Workflow:
1. Login as admin
2. Submit information (goes directly to active)
3. View active information (should see the info immediately)

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Account not approved yet"
}
```
or
```json
{
  "error": "Admin privileges required"
}
```

### 400 Bad Request
```json
{
  "password": ["Passwords do not match"]
}
```

### 404 Not Found
```json
{
  "error": "Pending information not found or already processed"
}
```

## File Upload Example

For uploading images with information:

```bash
curl -X POST http://localhost:8000/api/submit-info/ \
  -F "heading=Information with Image" \
  -F "description=This information includes an image" \
  -F "image=@/path/to/image.jpg" \
  -b cookies.txt
```

## Notes

- All requests require session cookies after login
- Use `-b cookies.txt` to send cookies from login
- Use `-c cookies.txt` to save cookies from login
- Admin endpoints require admin privileges (`is_user=True` or `is_superuser=True`)
- Regular users can only submit and view information
- Superusers can approve users and information