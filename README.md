# ShrinkShield

ShrinkShield is a portfolio project showcasing a modern backend architecture for detecting product shrinkflation and unit price spikes.  
It uses FastAPI, PostgreSQL, SQLAlchemy, and Alembic for migrations. Future milestones add OCR pipelines, size normalization, and a React/Next.js UI.

---

## Roadmap

- [x] Day 1: Containerized FastAPI backend with health endpoint  
- [x] Day 2: Postgres + Alembic migrations; basic data models  
- [x] Day 3: OCR pipeline scaffold (Donut/TrOCR) → parse sample receipts  
- [x] Day 4: Size normalization + unit price calculation  
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


## ✅ Day 3 Checkpoint — OCR Pipeline Scaffold

**What’s live now**

- Upload endpoint wired (`POST /receipts`)  
- Files saved to the database with metadata (filename, mimetype, size, uploaded_at)  
- OCR pipeline scaffold added (`ocr/adapter.py`)  
  - Currently uses a **stub engine** that returns placeholder OCR text  
  - Future: swap in Hugging Face Donut/TrOCR models for real parsing  
- Endpoints:  
  - `GET /receipts` → list all uploaded receipts  
  - `GET /receipts/{id}` → retrieve details + OCR output for a specific receipt  

**How to run**

```bash
cd infra
docker compose up --build -d
# logs (optional)
docker compose logs -f backend
```
**upload a sample file**
```
curl -X POST "http://localhost:8000/receipts" \
-F "file=@/path/to/sample-receipt.png"
```
**list stored receipts**
```
curl http://localhost:8000/receipts
```


## ✅ Day 4 Checkpoint — Size Normalization & Unit Pricing

**What’s live now**

- **Normalized sizes** → convert “1 L”, “500 mL”, “12oz”, etc. to **milliliters** (`utils/normalizer.py`)
- **Structured OCR lines** → stub now returns `{ name, size, price }` (extendable to real OCR later)
- **New table**: `product_lines` via Alembic migration  
  - columns: `id, receipt_id, name, raw_size, normalized_size_ml, price, unit_price_per_ml`
- **/receipts (POST)** now:
  - keeps Day 3 raw OCR lines (for readability)
  - **parses + normalizes** items
  - **computes unit price** (price ÷ normalized_size_ml)
  - saves structured rows to `product_lines`
- Endpoints:
  - `GET /receipts` → list uploaded receipts
  - `GET /receipts/{id}` → details including raw lines **and** structured `products[]`

**How to run**

```bash
cd infra
docker compose up --build -d
# logs (optional)
docker compose logs -f backend
```
**Upload a sample file**

```bash
curl -X POST "http://localhost:8000/receipts" \
  -F "file=@/path/to/sample-receipt.png"
```
