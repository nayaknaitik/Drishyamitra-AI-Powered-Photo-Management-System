## Drishyamitra

Production-quality AI photo management system.

### Project layout

- `backend/`: Flask API + AI pipelines + workers
- `frontend/`: React (Vite) web app
- `infra/`: Nginx reverse proxy config

### Run locally (Docker Compose)

Copy `.env.example` to `.env` if needed, then:

```bash
docker compose up --build
```

- **App**: `http://localhost/`
- **Backend health**: `http://localhost/api/health` (proxied to `backend:/health`)

### Migrations

In another terminal:

```bash
docker compose exec backend alembic upgrade head
```

### API quick reference

- **Auth**
  - `POST /api/auth/register`
  - `POST /api/auth/login`
- **Photos**
  - `POST /api/photos/upload` (multipart `file`)
  - `GET /api/photos`
  - `GET /api/photos/{id}`
  - `GET /api/photos/{id}/file`
- **Faces/Persons**
  - `POST /api/faces/label`
  - `GET /api/faces/persons`
- **Search**
  - `POST /api/search`
- **Chat**
  - `POST /api/chat`
- **Delivery**
  - `POST /api/send/email`
  - `POST /api/send/whatsapp`

