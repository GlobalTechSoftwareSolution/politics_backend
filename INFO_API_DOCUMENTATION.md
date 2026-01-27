# Information Submission and Approval API

This API allows users to submit information (with heading, description, and image) for approval, and administrators to approve or reject submissions.

## Overview

The system works with two main models:
- **PendingInfo**: Stores information submitted by users that needs approval
- **ActiveInfo**: Stores approved information that all users can view

## API Endpoints

### User Endpoints (Require Authentication)

#### 1. Submit Information
- **POST** `/api/submit-info/`
- **Description**: Submit new information for approval
- **Authentication**: Required (approved users only)
- **Request Body**:
```json
{
    "heading": "Information Title",
    "description": "Detailed description of the information",
    "image": "base64_encoded_image_or_file"  // Optional
}
```
- **Response**:
```json
{
    "message": "Information submitted successfully for approval",
    "pending_info": {
        "id": 1,
        "heading": "Information Title",
        "description": "Detailed description",
        "image": null,
        "submitted_by": { "id": 1, "email": "user@example.com", ... },
        "submitted_at": "2026-01-27T10:00:00Z",
        "status": "pending"
    }
}
```

#### 2. Get Active Information
- **GET** `/api/active-info/`
- **Description**: Get all approved information
- **Authentication**: Required (approved users only)
- **Response**:
```json
[
    {
        "id": 1,
        "heading": "Approved Title",
        "description": "Approved description",
        "image": null,
        "submitted_by": { "id": 1, "email": "user@example.com", ... },
        "approved_by": { "id": 2, "email": "admin@example.com", ... },
        "approved_at": "2026-01-27T10:00:00Z",
        "created_at": "2026-01-27T09:00:00Z"
    }
]
```

#### 3. Get My Submissions
- **GET** `/api/my-submissions/`
- **Description**: Get current user's pending and approved submissions
- **Authentication**: Required (approved users only)
- **Response**:
```json
{
    "pending_submissions": [
        {
            "id": 1,
            "heading": "Pending Title",
            "description": "Pending description",
            "image": null,
            "submitted_by": { "id": 1, "email": "user@example.com", ... },
            "submitted_at": "2026-01-27T10:00:00Z",
            "status": "pending"
        }
    ],
    "approved_submissions": [
        {
            "id": 1,
            "heading": "Approved Title",
            "description": "Approved description",
            "image": null,
            "submitted_by": { "id": 1, "email": "user@example.com", ... },
            "approved_by": { "id": 2, "email": "admin@example.com", ... },
            "approved_at": "2026-01-27T10:00:00Z",
            "created_at": "2026-01-27T09:00:00Z"
        }
    ]
}
```

### Admin Endpoints (Require Admin Privileges)

#### 1. Get Pending Information
- **GET** `/api/pending-info/`
- **Description**: Get all pending information that needs approval
- **Authentication**: Required (admin or superuser only)
- **Response**:
```json
[
    {
        "id": 1,
        "heading": "Pending Title",
        "description": "Pending description",
        "image": null,
        "submitted_by": { "id": 1, "email": "user@example.com", ... },
        "submitted_at": "2026-01-27T10:00:00Z",
        "status": "pending"
    }
]
```

#### 2. Approve Information
- **POST** `/api/approve-info/<id>/`
- **Description**: Approve a pending information submission
- **Authentication**: Required (admin or superuser only)
- **Response**:
```json
{
    "message": "Information approved successfully",
    "pending_info": {
        "id": 1,
        "heading": "Pending Title",
        "description": "Pending description",
        "image": null,
        "submitted_by": { "id": 1, "email": "user@example.com", ... },
        "submitted_at": "2026-01-27T10:00:00Z",
        "status": "approved"
    }
}
```

#### 3. Reject Information
- **POST** `/api/reject-info/<id>/`
- **Description**: Reject a pending information submission
- **Authentication**: Required (admin or superuser only)
- **Response**:
```json
{
    "message": "Information rejected successfully",
    "pending_info": {
        "id": 1,
        "heading": "Pending Title",
        "description": "Pending description",
        "image": null,
        "submitted_by": { "id": 1, "email": "user@example.com", ... },
        "submitted_at": "2026-01-27T10:00:00Z",
        "status": "rejected"
    }
}
```

## Authentication

The API uses session-based authentication (no JWT tokens). Users must:

1. **Register**: `POST /api/register/`
2. **Login**: `POST /api/login/`
3. **Use session cookies** for subsequent requests

### Admin Privileges

Users can approve information if they have:
- `is_superuser = True` (superuser)
- `is_user = True` (admin user)

Only superusers can approve other users and make them admins.

## Workflow Example

1. **User submits information**:
   ```bash
   curl -X POST http://localhost:8000/api/submit-info/ \
     -H "Content-Type: application/json" \
     -d '{"heading": "New Feature", "description": "Description of new feature"}'
   ```

2. **Admin views pending submissions**:
   ```bash
   curl http://localhost:8000/api/pending-info/
   ```

3. **Admin approves submission**:
   ```bash
   curl -X POST http://localhost:8000/api/approve-info/1/
   ```

4. **All approved users can view active information**:
   ```bash
   curl http://localhost:8000/api/active-info/
   ```

## Error Responses

- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions (not approved or not admin)
- **404 Not Found**: Resource not found
- **400 Bad Request**: Invalid data

## Models

### PendingInfo
- `heading`: String (max 200 chars)
- `description`: Text field
- `image`: Optional image upload
- `submitted_by`: Foreign key to User
- `submitted_at`: Auto timestamp
- `status`: 'pending', 'approved', or 'rejected'

### ActiveInfo
- `heading`: String (max 200 chars)
- `description`: Text field
- `image`: Optional image upload
- `submitted_by`: Foreign key to User (who submitted)
- `approved_by`: Foreign key to User (who approved)
- `approved_at`: When it was approved
- `created_at`: Auto timestamp

## File Uploads

Images can be uploaded as multipart form data. The API supports standard Django file upload handling.

## Database Schema

The system creates two new tables:
- `users_pendinginfo`: Stores pending submissions
- `users_activeinfo`: Stores approved information

Migration: `0006_activeinfo_pendinginfo.py`