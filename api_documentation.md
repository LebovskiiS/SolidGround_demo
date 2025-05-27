# API Documentation

## Base URL
All API endpoints are prefixed with `/api/v1/`.

## Authentication
Most endpoints require authentication using a token. Include the token in the request header:
```
Authorization: Token <your_token>
```

## User API

### User Registration
- **URL**: `/api/v1/user/registration/`
- **Method**: POST
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
  - Success (201 Created):
    ```json
    {
      "message": "User Created"
    }
    ```
  - Error (400 Bad Request):
    ```json
    {
      "username": ["error message"],
      "email": ["error message"],
      "password": ["error message"]
    }
    ```

### User Login
- **URL**: `/api/v1/user/login/`
- **Method**: POST
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  - Success (200 OK):
    ```json
    {
      "token": "string"
    }
    ```
  - Error (401 Unauthorized):
    ```json
    {
      "error": "Invalid credentials."
    }
    ```

### Get User Information
- **URL**: `/api/v1/user/{user_id}/`
- **Method**: GET
- **Authentication**: Required
- **Response**:
  - Success (200 OK):
    ```json
    {
      "id": "integer",
      "user": "integer",
      "username": "string",
      "age": "integer",
      "location": "string",
      "military_status": "boolean",
      "ptsd_level": "integer",
      "music": "integer",
      "therapist_contact": "integer",
      "scenario": "integer"
    }
    ```
  - Error (404 Not Found):
    ```json
    {
      "error": "UserInfo not found for this user."
    }
    ```

### Edit User Information
- **URL**: `/api/v1/user/edit/{user_id}/`
- **Method**: PATCH
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "age": "integer",
    "location": "string",
    "military_status": "boolean",
    "ptsd_level": "integer",
    "therapist_contact": "integer",
    "scenario": "integer"
  }
  ```
- **Response**:
  - Success (200 OK):
    ```json
    {
      "message": "UserInfo updated successfully.",
      "updated_data": {
        "age": "integer",
        "location": "string",
        "military_status": "boolean",
        "ptsd_level": "integer",
        "therapist_contact": "integer",
        "scenario": "integer"
      }
    }
    ```
  - Error (404 Not Found):
    ```json
    {
      "error": "UserInfo not found for this user."
    }
    ```

### Edit Emergency Contact
- **URL**: `/api/v1/user/edit/contact/{user_id}/`
- **Method**: PATCH
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "name": "string",
    "phone": "string",
    "email": "string",
    "relationship": "string"
  }
  ```
- **Response**:
  - Success (201 Created):
    ```json
    {
      "message": "A new emergency contact has been created.",
      "data": {
        "id": "integer",
        "name": "string",
        "phone": "string",
        "email": "string",
        "relationship": "string"
      }
    }
    ```
  - Error (400 Bad Request):
    ```json
    {
      "error": "The 'name', 'phone', and 'relationship' fields are required."
    }
    ```

### Get Music Tracks
- **URL**: `/api/v1/user/music/`
- **Method**: GET
- **Authentication**: Required
- **Response**:
  - Success (200 OK):
    ```json
    [
      {
        "id": "integer",
        "name": "string",
        "url": "string"
      }
    ]
    ```

### Set Music for User
- **URL**: `/api/v1/user/music/edit/{user_id}/`
- **Method**: POST
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "music": "integer"
  }
  ```
- **Response**:
  - Success (200 OK):
    ```json
    {
      "message": "Music track updated successfully"
    }
    ```
  - Error (404 Not Found):
    ```json
    {
      "error": "Music track not found"
    }
    ```

## Event API

### Trigger Alarm
- **URL**: `/api/v1/event/trigger/{user_id}/`
- **Method**: GET
- **Authentication**: Required
- **Response**:
  - Success (200 OK):
    ```json
    {
      "scenario": "string",
      "messages": [
        {"music_url": "string"},
        "string"
      ]
    }
    ```
  - Error (404 Not Found):
    ```json
    {
      "error": "User or UserInfo not found"
    }
    ```

## Chat API

### Send Message to GPT
- **URL**: `/api/v1/chat/{user_id}/`
- **Method**: POST
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "text": "string"
  }
  ```
- **Response**:
  - Success (200 OK):
    ```json
    {
      "response": "string"
    }
    ```
  - Error (400 Bad Request):
    ```json
    {
      "error": "Message text is required"
    }
    ```

### Get Support Chat WebSocket URL
- **URL**: `/api/v1/chat/user/support/{user_id}/`
- **Method**: GET
- **Authentication**: Required
- **Response**:
  - Success (200 OK):
    ```json
    {
      "user_id": "integer",
      "is_admin": "boolean",
      "websocket_url": "string"
    }
    ```
  - Error (404 Not Found):
    ```json
    {
      "error": "User not found"
    }
    ```

## WebSocket Connections

### Support Chat
- **URL**: `ws://127.0.0.1:8000/ws/chat/{user_id}/`
- **Authentication**: Token required in connection parameters
- **Message Format**:
  ```json
  {
    "message": "string"
  }
  ```