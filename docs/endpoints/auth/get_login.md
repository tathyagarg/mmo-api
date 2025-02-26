# GET /api/v1/auth/login

## Description
Logs in a user in the application

## Parameters

- `username` (string, body, required) - The username of the user
- `password` (string, body, required) - The password of the user

## Responses

- `200 OK` - The user has been logged in successfully 
- `422 Unprocessable Request` - The request is missing a required parameter
- `401 Unauthorized` - The username or password is incorrect
- `404 Not Found` - The user does not exist

## Example Request
```http
GET /api/v1/auth/login HTTP/1.1
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

{"message":"User logged in","data":{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc","token_type":"bearer"}}
```

## Prettier JSON Response
```json
{
  "message": "User logged in",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc",
    "token_type": "bearer"
  }
}
```

## Example `curl`

```bash
curl -X GET https://mmo.tathya.hackclub.app/api/v1/auth/login \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "password"}'
```

## Example `mcurl`
```bash
mcurl /auth/login -X GET -d '{"username": "johndoe", "password": "password"}'
```
