# Python Flask Microservice Application for the contents review

## Services
1. Authentication
2. Contents

## How to launch
- Install the `docker`
- Run the following command
   ```bash
   $ docker compose build
   $ docker compose up
   ```


## API Document

### auth-server

#### Retrieve API Status

   **Endpoint:** `GET /api/auth/status`

   **Description:** Retrieve the status of the API.

   **Example Request**
   ```http
   GET /api/auth/status HTTP/1.1
   Host: host
   ```

   **Example Responses**
   ```json
   {
      "code": 200,
      "data": null,
      "message": {
         "text": "OK",
         "status": "success",
         "show": false,
         "duration": 0
      }
   }
   ```

#### Signup

   **Endpoint:** `POST /api/auth/signup`

   **Description:** Register a new user.

   **Example Request:**
   ```http
   POST /api/auth/signup HTTP/1.1
   Host: example.com
   Content-Type: application/json

   {
      "email": "example@example.com",
      "password": "password123"
   }
   ```

   **Example Response:**
   ```json
   {
      "code": 200,
      "data": {
         "user_id": "43e374bb-9bd7-4faa-813f-c4917569c68f"
      },
      "message": {
         "duration": 0,
         "show": false,
         "status": "success",
         "text": "OK"
      }
   }
   ```

#### Login
   **Endpoint:** `POST /api/auth/login`

   **Description:** Authenticate a user and obtain access and refresh tokens.

   **Example Request:**
   ```http
   POST /api/auth/login HTTP/1.1
   Host: example.com
   Content-Type: application/json

   {
      "email": "example@example.com",
      "password": "password123"
   }
   ```

   **Example Response:**
   ```json
   {
      "code": 200,
      "data": {
         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwOTgxNzcxMCwianRpIjoiYzg2NmM4NTctY2Q5Mi00ZTE1LWI3YTctNGZkZDUzNWZiMmMyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQzZTM3NGJiLTliZDctNGZhYS04MTNmLWM0OTE3NTY5YzY4ZiIsIm5iZiI6MTcwOTgxNzcxMCwiY3NyZiI6IjgyMGI3ZWQ5LWVkNDktNGQ3ZC04MzJjLWY4MzE0NzVhY2M2ZCIsImV4cCI6MTcwOTkwNDExMH0.zIek_I5F7b36nkK10kipqJcPuNjMQsH3TPnmnFs23pQ",
         "created_date": 1709817595.0,
         "email": "example@example.com",
         "id": "43e374bb-9bd7-4faa-813f-c4917569c68f",
         "is_active": true,
         "modified_date": 0.0,
         "phone": null,
         "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwOTgxNzcxMCwianRpIjoiYTQxMmQzMjgtODZlMC00MTgwLTlhMDYtZTcyMWE2ZDBlYzNiIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI0M2UzNzRiYi05YmQ3LTRmYWEtODEzZi1jNDkxNzU2OWM2OGYiLCJuYmYiOjE3MDk4MTc3MTAsImNzcmYiOiI4NGM4NmI2Yi00NTM0LTQyZDUtODFkMS0yMjkyY2JlNTkzOTYiLCJleHAiOjE3MTAyNDk3MTB9.Q-fhoUfJz-abX_j1HJkmiPLbGBFkjKgI8V8Wehj5RvU"
      },
      "message": {
         "duration": 0,
         "show": false,
         "status": "success",
         "text": "Logged in successfully!"
      }
   }
   ```

#### Validate Token
   **Endpoint:** `GET /api/auth/tokens/validate`

   **Description:** Validate the access token.

   **Example Request:**
   ```http
   GET /api/auth/tokens/validate HTTP/1.1
   Host: example.com
   Authorization: Bearer <your_access_token>
   ```

   **Example Response:**
   ```json
   {
      "code": 200,
      "data": {
         "csrf": "820b7ed9-ed49-4d7d-832c-f831475acc6d",
         "exp": 1709904110,
         "fresh": false,
         "iat": 1709817710,
         "jti": "c866c857-cd92-4e15-b7a7-4fdd535fb2c2",
         "nbf": 1709817710,
         "sub": "43e374bb-9bd7-4faa-813f-c4917569c68f",
         "type": "access"
      },
      "message": {
         "duration": 0,
         "show": false,
         "status": "success",
         "text": "Token valid"
      }
   }
   ```

### contents-server

#### Retrieve API Status

   **Endpoint:** `GET /api/contents/status`

   **Description:** Retrieve the status of the API.

   **Example Request**
   ```http
   GET /api/contents/status HTTP/1.1
   Host: host
   ```

   **Example Responses**
   ```json
   {
      "code": 200,
      "data": null,
      "message": {
         "text": "OK",
         "status": "success",
         "show": false,
         "duration": 0
      }
   }
   ```

#### Retrieve All Contents
   **Endpoint:** `GET /api/contents/`
   **Description:** Retrieve all contents optionally filtered by `created_by` and `reviewed_by`.

   **Example Request**
   ```http
   GET /api/contents/?created_by=user123 HTTP/1.1
   Host: example.com
   ```

   **Example Responses**
   ```json
   {
      "code": 200,
      "data": [
         {
            "content": "Lorem ipsum dolor sit amet...",
            "created_by": "user123",
            "review": null,
            "reviewed_by": null,
            "id": 1,
            "title": "Content Title"
         }
      ],
      "message": {
         "text": "OK",
         "status": "success",
         "show": false,
         "duration": 0
      }
   }
   ```

#### Retrieve Content by ID
   **Endpoint:** `GET /api/contents/{content_id}`

   **Description:** Retrieve content by its ID.

   **Example Request:**
   ```http
   GET /api/contents/1 HTTP/1.1
   Host: example.com
   ```
   **Example Response:**
   ```json
   {
      "code": 200,
      "data": {
         "content": "Lorem ipsum dolor sit amet...",
         "created_by": "user123",
         "reviewed_by": null,
         "id": 1,
         "title": "Content Title"
      },
      "message": {
         "text": "OK",
         "status": "success",
         "show": false,
         "duration": 0
      }
   }
   ```

#### Create New Content
   **Endpoint:** `POST /api/contents/`

   **Description:** Create new content.

   **Example Request:**
   ```http
   POST /api/contents/ HTTP/1.1
   Host: example.com
   Content-Type: application/json
   Authorization: Bearer <your_access_token>

   {
      "title": "New Content",
      "content": "Lorem ipsum dolor sit amet...",
      "created_by": "user123"
   }
   ```

   **Example Response:**
   ```json
   {
      "code": 200,
      "data": {
         "content": "Lorem ipsum dolor sit amet...",
         "created_by": "user123",
         "review": null,
         "reviewed_by": null,
         "id": 2,
         "title": "New Content"
      },
      "message": {
         "text": "OK",
         "status": "success",
         "show": false,
         "duration": 0
      }
   }
   ```

#### Review Content
   **Endpoint:** `PUT /api/contents/{content_id}`

   **Description:** Review existing content.

   **Example Request:**
   ```http
   PUT /api/contents/2 HTTP/1.1
   Host: example.com
   Content-Type: application/json
   Authorization: Bearer <your_access_token>

   {
      "review": "Content reviewed and approved."
   }
   ```

#### Delete Content
   **Endpoint:** `DELETE /api/contents/{content_id}`

   **Description:** Delete content by its ID.

   **Example Request:**
   ```http
   DELETE /api/contents/2 HTTP/1.1
   Host: example.com
   Authorization: Bearer <your_access_token>
   ```

   **Example Response:**
   ```json
   {
      "code": 200,
      "data": null,
      "message": {
         "text": "OK",
         "status": "success",
         "show": false,
         "duration": 0
      }
   }
   ```
