# Python Flask Microservice Application for the contents review

## Services
1. Authentication
2. Contents

## How to launch
- Install the `docker`
- Run the following command
    - Windows
        ```cmd
        $ docker-compose build
        $ docker-compose up
        ```
    - Ubutnu
        ```shell
        $ docker compose build
        $ docker compose up
        ```


## API Document

### auth-server
1. Status 

    **Description** : Get current status of the server
    
    **URL** : `/api/auth/status`

    **Method** : `GET`

    **Auth required** : NO

    ### Success Response

      **Condition** : If everything is OK.
      **Code** : `200 OK`

**Content example**
json { "status": True }

## Create New User

Create new User

**URL** : `YOUR_HOST/signup`

**Method** : `POST`

**Auth required** : NO

**Data constraints**
json { "email": "[valid email address]", "password": "[password in plain text]" }

### Success Response

**Condition** : If everything is OK.

**Code** : `200 OK`

**Content example**
json { "user_id": "6037f1f0-02b2-42a7-be8b-5f0c22b1e34b" }

## User Login 

Authenticate a User.

**URL** : `YOUR_HOST/login`

**Method** : `POST`

**Auth required** : NO

**Data constraints**
json { "email": "[valid email address]", "password": "[password in plain text]" }

### Success Response

**Condition** : If the user is found in the database and password matches.

**Code** : `200 OK`

**Content example**

The access_token and refresh_token are unique to each unique login request.
json { "accesstoken": "abc.def.ghi", "refreshtoken": "jkl.mno.pqr", "username": "johndoe" }

## Validate Token 

Validate the access token.

**URL** : `YOUR_HOST/tokens/validate`

**Method** : `GET`

**Auth required** : YES

**Headers**
Authorization: "Bearer abc.def.ghi"

### Success Response

**Condition** : If the token is valid.

**Code** : `200 OK`

**Content example**
json { "message": "Token valid", "data": {…payload} }
