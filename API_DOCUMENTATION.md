# Politics Backend API Documentation

Complete API reference with curl examples for Postman and frontend development.

## Base URL

```
http://127.0.0.1:8000
```

## Authentication

**Session-based authentication** - No JWT tokens required.

- Login creates a session cookie
- Subsequent requests use the session cookie
- Admin endpoints require admin privileges
- No token management needed

## API Endpoints

### 1. User Registration

**Endpoint:** `POST /api/register/`

**Description:** Register a new user account

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "fullname": "John Doe",
    "role": "user"
}
```

**Curl Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "fullname": "John Doe",
    "role": "user"
  }'
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully. Please wait for approval.",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "fullname": "John Doe",
        "role": "user",
        "is_approved": false,
        "is_user": false,
        "is_superuser": false,
        "created_at": "2026-01-27T10:30:00Z",
        "approval_date": null
    }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid data or passwords don't match
- `409 Conflict` - Email already exists

---

### 2. User Login

**Endpoint:** `POST /api/login/`

**Description:** Login with email and password (session-based)

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Curl Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "fullname": "John Doe",
        "role": "user",
        "is_approved": true,
        "is_user": false,
        "is_superuser": false
    },
    "note": "Session-based authentication - no JWT tokens"
}
```

**Error Responses:**
- `400 Bad Request` - Missing email or password
- `401 Unauthorized` - Invalid credentials
- `403 Forbidden` - Account not approved yet

---

### 3. User Profile

**Endpoint:** `GET /api/profile/`

**Description:** Get current user profile (requires login)

**Curl Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Content-Type: application/json" \
  -b "sessionid=<session_cookie>"
```

**Response (200 OK):**
```json
{
    "message": "User profile retrieved successfully",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "fullname": "John Doe",
        "role": "user",
        "is_approved": true,
        "is_user": false,
        "is_superuser": false,
        "created_at": "2026-01-27T10:30:00Z",
        "updated_at": "2026-01-27T10:35:00Z",
        "approval_date": "2026-01-27T10:40:00Z"
    },
    "note": "Session-based authentication working"
}
```

**Error Responses:**
- `401 Unauthorized` - Not logged in

---

### 4. Pending Users (Admin Only)

**Endpoint:** `GET /api/pending-users/`

**Description:** Get list of users waiting for approval (admin only)

**Curl Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/pending-users/ \
  -H "Content-Type: application/json" \
  -b "sessionid=<admin_session_cookie>"
```

**Response (200 OK):**
```json
[
    {
        "id": 2,
        "email": "pending@example.com",
        "fullname": "Jane Smith",
        "role": "user",
        "created_at": "2026-01-27T10:40:00Z",
        "is_approved": false,
        "is_user": false,
        "is_superuser": false
    },
    {
        "id": 3,
        "email": "another@example.com",
        "fullname": "Bob Johnson",
        "role": "user",
        "created_at": "2026-01-27T10:45:00Z",
        "is_approved": false,
        "is_user": false,
        "is_superuser": false
    }
]
```

**Error Responses:**
- `401 Unauthorized` - Not logged in
- `403 Forbidden` - Not admin

---

### 5. Approve User (Admin Only)

**Endpoint:** `POST /api/approve-user/{user_id}/`

**Description:** Approve a user and optionally make them admin

**Curl Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/approve-user/2/ \
  -H "Content-Type: application/json" \
  -b "sessionid=<admin_session_cookie>"
```

**Response (200 OK):**
```json
{
    "message": "User pending@example.com has been approved and made admin",
    "user": {
        "id": 2,
        "email": "pending@example.com",
        "fullname": "Jane Smith",
        "role": "admin",
        "is_approved": true,
        "is_user": true,
        "is_superuser": false,
        "approval_date": "2026-01-27T10:50:00Z"
    }
}
```

**Error Responses:**
- `401 Unauthorized` - Not logged in
- `403 Forbidden` - Not admin
- `404 Not Found` - User not found

---

### 6. Protected Endpoint (Public)

**Endpoint:** `GET /api/protected/`

**Description:** Public endpoint accessible to all (no auth required)

**Curl Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/protected/
```

**Response (200 OK):**
```json
{
    "message": "Welcome to the protected area!",
    "note": "Authentication removed - no JWT tokens required"
}
```

---

## Postman Collection Setup

### 1. Create Environment Variables

Set these variables in Postman:

```
baseUrl: http://127.0.0.1:8000
sessionCookie: (will be set after login)
```

### 2. Login Request (Set Session Cookie)

**Request:**
- Method: POST
- URL: `{{baseUrl}}/api/login/`
- Body: Raw JSON

**Tests (Set Session Cookie):**
```javascript
pm.test("Login successful", function () {
    pm.expect(pm.response.code).to.eql(200);
});

// Extract session cookie
var cookies = pm.cookies.toObject();
if (cookies.sessionid) {
    pm.environment.set("sessionCookie", cookies.sessionid);
}
```

### 3. Subsequent Requests

Add this to the **Headers** of requests that require authentication:

```
Cookie: sessionid={{sessionCookie}}
```

## Frontend Integration Examples

### React/JavaScript Example

```javascript
// Register user
const registerUser = async (userData) => {
    const response = await fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    return response.json();
};

// Login user
const loginUser = async (email, password) => {
    const response = await fetch('/api/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
    });
    return response.json();
};

// Get user profile
const getUserProfile = async () => {
    const response = await fetch('/api/profile/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    return response.json();
};

// Get pending users (admin)
const getPendingUsers = async () => {
    const response = await fetch('/api/pending-users/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    return response.json();
};

// Approve user (admin)
const approveUser = async (userId) => {
    const response = await fetch(`/api/approve-user/${userId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
    return response.json();
};
```

### Error Handling

```javascript
// Check if user needs approval
if (response.status === 403 && response.error === "Account not approved yet. Please contact admin for approval.") {
    // Show approval pending message
}

// Check if not logged in
if (response.status === 401) {
    // Redirect to login
}

// Check if not admin
if (response.status === 403 && response.error === "Admin access required") {
    // Show access denied
}
```

## Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied (not approved/not admin)
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (email exists)

## Notes

- **No JWT tokens** - Uses session-based authentication
- **Session cookies** handle authentication automatically
- **Admin privileges** required for user management
- **Approval workflow** for new users
- **Production-ready** authentication system