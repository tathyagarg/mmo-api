# MMO API Documentation

- All endpoints in the API (not docs) are prefixed with `api/v1`
- The `docs/endpoints` directory contains API documentation for each endpoint in the MMO API. Each file is named after the endpoint it documents.

## Endpoints
1. `POST /oauth2` - [OAuth 2.0](endpoints/post_oauth2.md)

## `mcurl` 
Run the following command to download mcurl:
```bash
curl -o mcurl https://mmo.tathya.hackclub.app/mcurl
```
After downloading `mcurl`, run:
```bash
mcurl set <access_token> 
```
Where `<access_token>` is the token you get from [POST /oauth2](endpoints/post_oauth2.md).


## Authentication

The MMO API uses OAuth 2.0 for authentication. To authenticate, you must first obtain an access token (refer to [POST /oauth2](endpoints/post_oauth2.md)).  Once you have an access token, you can either:

1. Use regular curl and include it in the `Authorization` header of each request to the API. The value of the `Authorization` header should be `Bearer <access_token>`, where `<access_token>` is the access token you obtained.

2. Use [`mcurl`](##mcurl) to make authenticated requests to the API. `mcurl` is a command-line tool that simplifies making authenticated requests to the MMO API. To use `mcurl`, you must first obtain an access token and set it using the `mcurl set <access_token>` command. After setting the token, you can make authenticated requests to the API using `mcurl <endpoint>`, where `<endpoint>` is the endpoint you want to access (not the full URL, and without `/api/v1`).

