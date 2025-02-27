# PUT /api/v1/player/move/{direction}

Move the player in the specified direction

## Parameters

- `direction` (string, path, required) - The direction in which the player should move. Options:
  - `north`
  - `south`
  - `east`
  - `west`

## Responses

- `200 OK` - The player has been moved successfully
- `422 Unprocessable Request` - The request is missing a required Parameters
- `400 Bad Request` - The direction is invalid
- `401 Unauthorized` - The user is not authenticated

## Example Request

```http
PUT /api/v1/player/move/north HTTP/1.1
Accept: application/json
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc
```

## Example Response

```http
HTTP/1.1 200 OK
Content-Length: 204
Content-Type: application/json

{"username":"johndoe","data":{"x":0,"y":1}}
```

## Prettier JSON Response

```json
{
  "username": "johndoe",
  "data": {
    "x": 0,
    "y": 1
  }
}
```

## Example `curl`

```bash
curl -X PUT https://mmo.tathya.hackclub.app/api/v1/player/move/north \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNzQwNjQ2NzE1fQ.nW9zfG2hDbOKN0Knaw4oyf4nczhLHfJjQhO7AFB04Lc"
```

## Example `mcurl`

```bash
mcurl /player/move/north -X PUT
```
