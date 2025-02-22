Allows you to signup or login to the application

## POST /api/v1/token

### Parameters

- `username` (string, body, required) - The username of the user
- `password` (string, body, required) - The password of the user

### Responses

- `200 OK` - The user has been authenticated successfully
- `422 Unprocessable Request` - The request is missing a required parameter
- `401 Unauthorized` - The user could not be authenticated

### Example Request
```http
POST /api/v1/token HTTP/1.1
Accept: application/json
Content-Type: application/x-www-form-urlencoded

grant_type=password&username=2awesome&password=sauce&scope=&client_id=&client_secret=
```

### Example Response

```http
HTTP/1.1 200 OK
Content-Length: 169
Content-Type: application/json
Date: Tue, 23 Feb 2025 21:30:00 GMT

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyYXdlc29tZSIsImV4cCI6MTc0MDI2MTM5OH0.g1hm6YRglfpG2MMiZRg8kF2Mh0ezfdlV7IeNC6qz_H8",
  "token_type": "bearer"
}
```
