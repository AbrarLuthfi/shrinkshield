## Roadmap

- [x] Day 1: Containerized FastAPI backend with health endpoint
- [x] Day 2: Postgres + Alembic migrations; basic data models
- [ ] Day 3: OCR pipeline scaffold (Donut/TrOCR) → parse sample receipts
- [ ] Day 4: Size normalization + unit price calculation
- [ ] Day 5: Web UI scaffold (Next.js) + upload flow
- [ ] Day 6: Alerts logic (shrink & unit-price spike) + tests
- [ ] Day 7: Deploy preview + demo video


---


## ✅ Day 2 Checkpoint — Database Online

**What’s live now**

Docker Compose runs **Postgres 16** and the **FastAPI backend**
SQLAlchemy wired up (`app/db.py`, `app/models.py`)
Tables auto-created on startup (dev)
Basic DB endpoints:
`GET /health` → service health
`GET /db/ping` → DB connection check
`POST /db/sample-user` → inserts `demo@example.com` into `users`

**How to run**

`cd infra`
`docker compose up --build -d`
`# logs (optional)`
`docker compose logs -f backend`


### Database migrations with Alembic

- Create new migration after editing models:
  ```bash
  docker compose exec backend bash -lc 'cd /app && alembic -c /app/alembic.ini revision --autogenerate -m "describe change"'
