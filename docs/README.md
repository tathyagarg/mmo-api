# MMO API Documentation

- All endpoints in the API are prefixed with `api/v1`
- The `endpoints` directory contains API documentation for each endpoint in the MMO API. Each file is named after the endpoint it documents.

## Authentication

The MMO API uses OAuth 2.0 for authentication. To authenticate, you must first obtain an access token (refer to [POST /oauth2](endpoints/post_oauth2.md)). Once you have an access token, you must include it in the `Authorization` header of each request to the API. The value of the `Authorization` header should be `Bearer <access_token>`, where `<access_token>` is the access token you obtained.
