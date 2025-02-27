# GET /api/v1/player/me

Get the current player's information

## Parameters

- `Authorization` (string, header, required) - The JWT token of the player

## Responses

- `200 OK` - The player's information has been retrieved successfully
- `401 Unauthorized` - The JWT token is invalid or expired

## Example Request
```http
GET /api/v1/player/me HTTP/1.1
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Length: 204
Content-Type: application/json

{"username":"johndoe","data":{}}
```

## Prettier JSON Response
```json
{
  "username": "johndoe",
  "data": {}
}
```

## Example `curl`

```bash
curl -X GET https://mmo.tathya.hackclub.app/api/v1/player/me \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc"
```

## Example `mcurl`
```bash
mcurl /player/me -X GET
```
