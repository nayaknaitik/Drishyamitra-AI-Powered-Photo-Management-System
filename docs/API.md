## Drishyamitra API

Base URL: behind Nginx, all endpoints are under `/api/*`.

### Auth

#### POST `/api/auth/register`

Body:

```json
{ "email": "user@example.com", "password": "secret" }
```

Response:

```json
{ "user": { "id": 1, "email": "user@example.com" }, "access_token": "..." }
```

#### POST `/api/auth/login`

Same shape as register.

### Photos

#### POST `/api/photos/upload`

Multipart form-data: `file=<image>`

Response:

```json
{
  "photo_id": 123,
  "faces": [
    { "id": 1, "x": 10, "y": 20, "w": 90, "h": 90, "is_unknown": true, "person_id": null, "person_name": null }
  ]
}
```

#### GET `/api/photos`

Response:

```json
{ "items": [ { "id": 123, "taken_at": null, "created_at": "...", "original_filename": "a.jpg" } ] }
```

#### GET `/api/photos/{id}/file`

Returns the image bytes. Requires `Authorization: Bearer <token>`.

### Faces / Persons

#### POST `/api/faces/label`

Body:

```json
{ "face_id": 1, "person_name": "Mom" }
```

#### GET `/api/faces/persons`

### Search

#### POST `/api/search`

Body:

```json
{ "query": "Show photos of Mom from last year" }
```

### Chat

#### POST `/api/chat`

Body:

```json
{ "message": "show photos of mom" }
```

### Delivery

#### POST `/api/send/email`

Body:

```json
{ "to": "dest@example.com", "photo_ids": [123, 124] }
```

#### POST `/api/send/whatsapp`

Body:

```json
{ "to": "+15551234567", "photo_ids": [123, 124] }
```

