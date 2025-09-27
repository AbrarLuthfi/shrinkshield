# ShrinkShield

ShrinkShield is a portfolio project showcasing a modern backend architecture for detecting product shrinkflation and unit price spikes.  
It uses FastAPI, PostgreSQL, SQLAlchemy, and Alembic for migrations. Future milestones add OCR pipelines, size normalization, and a React/Next.js UI.

---

## Roadmap

- [x] Day 1: Containerized FastAPI backend with health endpoint  
- [x] Day 2: Postgres + Alembic migrations; basic data models  
- [ ] Day 3: OCR pipeline scaffold (Donut/TrOCR) → parse sample receipts  
- [ ] Day 4: Size normalization + unit price calculation  
- [ ] Day 5: Web UI scaffold (Next.js) + upload flow  
- [ ] Day 6: Alerts logic (shrink & unit-price spike) + tests  
- [ ] Day 7: Deploy preview + demo video  

---

## ✅ Day 1 Checkpoint — Backend Skeleton

**What’s live now**

- FastAPI backend containerized with Docker  
- Health check endpoint:  
  - `GET /health` → returns `{"status": "ok", "message": "ShrinkShield backend is running 🚀"}`  

**How to run**

```bash
cd infra
docker compose up --build -d
curl http://localhost:8000/health
```


## ✅ Day 2 Checkpoint — Database Online

**What’s live now**

- Docker Compose runs **Postgres 16** and the **FastAPI backend**  
- SQLAlchemy wired up (`app/db.py`, `app/models.py`)  
- Tables managed by **Alembic migrations**  
- Basic DB endpoints:  
  - `GET /health` → service health  
  - `GET /db/ping` → DB connection check  
  - `POST /db/sample-user` → inserts `demo@example.com` into `users`  

**How to run**

```bash
cd infra
docker compose up --build -d
# logs (optional)
docker compose logs -f backend
```
