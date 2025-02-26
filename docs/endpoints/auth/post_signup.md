# POST /api/v1/auth/signup

## Description
Creates a new user in the application

## Parameters

- `username` (string, body, required) - The username of the user
- `password` (string, body, required) - The password of the user

## Responses

- `201 Created` - The user has been created successfully
- `422 Unprocessable Request` - The request is missing a required parameter
- `409 Conflict` - The username is already taken

## Example Request
```http
GET /api/v1/auth/signup HTTP/1.1
Accept: application/json
Content-Type: application/json

{
  "username": "johndoe",
  "password": "password"
}
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Length: 204 
Content-Type: application/json
Date: Tue, 23 Feb 2025 21:30:00 GMT

{"message":"User created","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc","token_type":"bearer"}}
```

## Prettier JSON Response
```json
{
  "message": "User created",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc",
    "token_type": "bearer"
  }
}
```

## Example `curl`

```bash
curl -X POST https://mmo.tathya.hackclub.app/api/v1/auth/signup \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "password"}'
```

## Example `mcurl`
```bash
mcurl /auth/signup -X POST -d '{"username": "johndoe", "password": "password"}'
```
