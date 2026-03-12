## Database schema (logical)

### `users`
- `id` (PK)
- `email` (unique)
- `password_hash`

### `photos`
- `id` (PK)
- `user_id` → `users.id`
- `file_path`
- `original_filename`
- `mime_type`
- `taken_at`
- `metadata_json` (EXIF, etc.)

### `persons`
- `id` (PK)
- `user_id` → `users.id`
- `name`

### `faces`
- `id` (PK)
- `user_id` → `users.id`
- `photo_id` → `photos.id`
- `person_id` → `persons.id` (nullable)
- `embedding_id` → `face_embeddings.id` (nullable)
- bbox: `x,y,w,h`
- `detection_confidence`
- `is_unknown`

### `face_embeddings`
- `id` (PK)
- `user_id` → `users.id`
- `model_name` (Facenet512)
- `detector_backend` (RetinaFace)
- `vector_dim`
- `embedding_encrypted` (bytes)

### `photo_tags`
- `id` (PK)
- `user_id` → `users.id`
- `photo_id` → `photos.id`
- `key` / `value`

### `delivery_logs`
- `id` (PK)
- `user_id` → `users.id`
- `channel` (email|whatsapp)
- `destination`
- `status` (queued|sent|failed)
- `provider_message_id`
- `error_message`

### `chat_history`
- `id` (PK)
- `user_id` → `users.id`
- `role`
- `content`

### Relationships

- photo → faces (1:N)
- face → person (N:1)
- person → faces → photos (via join)

