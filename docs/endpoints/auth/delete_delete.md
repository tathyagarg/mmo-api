# DELETE /api/v1/auth/delete

Deletes the user account

## Parameters

- `username` (string, body, required) - The username of the user
- `password` (string, body, required) - The password of the user

## Responses

- `200 OK` - The user has been deleted successfully
- `422 Unprocessable Request` - The request is missing a required Parameters
- `401 Unauthorized` - The username or password is incorrect
- `404 Not Found` - The user does not exist

## Example Request

```http
DELETE /api/v1/auth/delete HTTP/1.1
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
Content-Length: 27 
Content-Type: application/json

{"message":"User deleted"}
```

## Prettier JSON Response

```json
{
  "message": "User deleted"
}
```

## Example `curl`

```bash
curl -X DELETE https://mmo.tathya.hackclub.app/api/v1/auth/delete \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "password"}'
```

## Example `mcurl`

```bash
mcurl /auth/delete -X DELETE -d '{"username": "johndoe", "password": "password"}'
```
