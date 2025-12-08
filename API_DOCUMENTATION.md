# GrantGuru API Documentation

## Overview
GrantGuru is a web application designed to help users discover and apply for grants. The backend API provides endpoints for authentication, grant discovery, application management, and user profile management.

**Base URL:** `http://localhost:5000`  
**Version** December 8, 2025

---

## Quick Reference: Endpoints Summary

| Method | Path | Auth Required |
|--------|------|---------------|
| POST | /api/auth/signup | No | 
| POST | /api/auth/signin | No |
| GET | /api/public/search_grants | No |
| GET | /api/applications/grants | No | 
| GET | /api/applications/user/{user_id} | No |
| POST | /api/applications/create | No | 
| PUT | /api/user/personal-info | JWT |  
| PUT | /api/user/password | JWT |

---

## Authentication & Headers

### JWT Bearer Token

All protected endpoints require a JWT Bearer token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

**Protected Routes:**
- `PUT /api/user/personal-info`
- `PUT /api/user/password`

**Public Routes (No Auth Required):**
- `POST /api/auth/signup`
- `POST /api/auth/signin`
- `GET /api/public/search_grants`
- `GET /api/applications/grants`
- `GET /api/applications/user/{user_id}`
- `POST /api/applications/create`

---

## Response Format

### Standard Success Response
```json
{
  "status": "success",
  "data": { /* endpoint-specific data */ }
}
```

### Standard Error Response
```json
{
  "status": "error",
  "message": "Human-readable error message"
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource successfully created |
| 400 | Bad Request - Missing or invalid fields |
| 401 | Unauthorized - Invalid credentials or missing/invalid JWT |
| 409 | Conflict - Resource already exists (e.g., duplicate email) |
| 500 | Internal Server Error - Database or server error |

---

## API Endpoints

### 1. Authentication Endpoints

#### POST /api/auth/signup
Creates a new user account.

**Request Body:**
```json
{
  "f_name": "John",
  "m_name": "Michael",
  "l_name": "Doe",
  "email": "john.doe@example.com",
  "password": "ASecurePassword!",
  "institution": "University of Southern Maine"
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "data": {
    "user_id": "12345",
    "email": "john.doe@example.com",
    "f_name": "John",
    "m_name": "Michael",
    "l_name": "Doe",
    "institution": "University of Southern Maine",
    "access_token": "<TOKEN>"
  }
}
```

**Status Codes:**
- `201 Created` — User successfully registered
- `400 Bad Request` — Missing required fields or invalid format
- `409 Conflict` — Email already registered
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/auth/routes_auth.py`](Phase3_work/api/auth/routes_auth.py)

---

#### POST /api/auth/signin
Authenticates a user and returns a JWT token.

**Request Body:**
```json
{
  "email": "john.doe@example.com",
  "password": "ASecurePassword!"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "user_id": "12345",
    "email": "john.doe@example.com",
    "f_name": "John",
    "m_name": "Michael",
    "l_name": "Doe",
    "institution": "University of Southern Maine",
    "access_token": "<Token>"
  }
}
```

**Status Codes:**
- `200 OK` — Login successful
- `400 Bad Request` — Missing email or password
- `401 Unauthorized` — Invalid email or password
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/auth/routes_auth.py`](Phase3_work/api/auth/routes_auth.py)

---

### 2. Public Grant Discovery Endpoints

#### GET /api/public/search_grants
Searches for grants based on query parameters.

**Query Parameters:**
| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `q` | string | No | "" | Search query (searches grant title and description) |
| `page` | integer | No | 1 | Page number for pagination |
| `page_size` | integer | No | 10 | Results per page (min: 1, max: 100) |

**Example Request:**
```
GET /api/public/search_grants?q=STEM+education&page=1&page_size=20
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "grants": [
      {
        "grant_id": "G001",
        "title": "STEM Education Excellence",
        "description": "Support for innovative STEM programs",
        "amount": 50000,
        "deadline": "2025-06-30"
      }
    ],
    "total_results": 150,
    "page": 1,
    "page_size": 20,
    "total_pages": 8
  }
}
```

**Status Codes:**
- `200 OK` — Search successful
- `400 Bad Request` — Invalid page or page_size parameters
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/public/routes_public.py`](Phase3_work/api/public/routes_public.py)

---

#### GET /api/applications/grants
Retrieves all available grants (no filtering).

**Query Parameters:**
| Parameter | Type | Default |
|-----------|------|---------|
| `page` | integer | 1 |
| `page_size` | integer | 10 |

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "grants": [
      {
        "grant_id": "G001",
        "title": "STEM Education Excellence",
        "description": "Support for innovative STEM programs",
        "amount": 50000,
        "deadline": "2025-06-30",
        "agency": "National Science Foundation"
      }
    ],
    "total_results": 250,
    "page": 1,
    "page_size": 10,
    "total_pages": 25
  }
}
```

**Status Codes:**
- `200 OK` — Grants retrieved successfully
- `400 Bad Request` — Invalid pagination parameters
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/applications/routes_applications.py`](Phase3_work/api/applications/routes_applications.py)

---

### 3. User Grant Applications Endpoints

#### GET /api/applications/user/{user_id}
Retrieves all grant applications submitted by a specific user.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | string | The unique identifier of the user |

**Example Request:**
```
GET /api/applications/user/12345
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "user_id": "12345",
    "applications": [
      {
        "application_id": "A001",
        "grant_id": "G001",
        "grant_title": "STEM Education Excellence",
        "status": "submitted",
        "submission_date": "2025-01-15",
        "grant_amount": 50000,
        "deadline": "2025-06-30",
        "notes": "Applied for educational program funding"
      }
    ],
    "total_applications": 5
  }
}
```

**Status Codes:**
- `200 OK` — Applications retrieved successfully
- `404 Not Found` — User not found
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/applications/routes_applications.py`](Phase3_work/api/applications/routes_applications.py)

---

#### POST /api/applications/create
Creates a new grant application.

**Request Body:**
```json
{
  "user_id": "12345",
  "grant_id": "G001",
  "notes": "Our institution is well-positioned to implement this STEM program"
}
```

**Response (201 Created):**
```json
{
  "status": "success",
  "data": {
    "application_id": "A001",
    "user_id": "12345",
    "grant_id": "G001",
    "status": "submitted",
    "submission_date": "2025-01-15T10:30:00Z",
    "notes": "Our institution is well-positioned to implement this STEM program"
  }
}
```

**Status Codes:**
- `201 Created` — Application successfully created
- `400 Bad Request` — Missing required fields (user_id, grant_id)
- `404 Not Found` — User or grant not found
- `409 Conflict` — User already applied for this grant
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/applications/routes_applications.py`](Phase3_work/api/applications/routes_applications.py)

---

### 4. User Profile Management Endpoints

#### PUT /api/user/personal-info
Updates user personal information. **Requires JWT authentication.**

**Authorization Header:**
```http
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "f_name": "John",
  "m_name": "Michael",
  "l_name": "Doe",
  "institution": "MIT"
}
```

**Notes:** All fields are optional. Only provided fields will be updated.

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "user_id": "12345",
    "f_name": "John",
    "m_name": "Michael",
    "l_name": "Doe",
    "institution": "University of Southern Maine",
    "email": "john.doe@example.com"
  }
}
```

**Status Codes:**
- `200 OK` — User information successfully updated
- `400 Bad Request` — Invalid field values
- `401 Unauthorized` — Missing or invalid JWT token
- `404 Not Found` — User not found
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/user/routes_user.py`](Phase3_work/api/user/routes_user.py)

---

#### PUT /api/user/password
Updates user password. **Requires JWT authentication.**

**Authorization Header:**
```http
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "oldPassword": "CurrentPassword123!",
  "newPassword": "NewSecurePassword456!"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Password successfully updated"
}
```

**Status Codes:**
- `200 OK` — Password successfully updated
- `400 Bad Request` — Missing required fields or password too weak
- `401 Unauthorized` — Missing JWT token or incorrect old password
- `404 Not Found` — User not found
- `500 Internal Server Error` — Database error

**Implementation:** [`Phase3_work/api/user/routes_user.py`](Phase3_work/api/user/routes_user.py)

---

## Frontend Integration

The following frontend components interact with these API endpoints:

- **AuthDialog.tsx** — Calls `/api/auth/signup` and `/api/auth/signin`
- **GrantsSearchPage.tsx** — Calls `/api/public/search_grants` and `/api/applications/create`
- **ApplicationDetailsPage.tsx** — Calls `/api/applications/user/{user_id}`
- **UserProfilePage.tsx** — Calls `/api/user/personal-info` and `/api/user/password`
