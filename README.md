# ShrinkShield

ShrinkShield is a portfolio project showcasing a modern backend architecture for detecting product shrinkflation and unit price spikes.  
It uses FastAPI, PostgreSQL, SQLAlchemy, and Alembic for migrations. Future milestones add OCR pipelines, size normalization, and a React/Next.js UI.

---

## Roadmap

- [x] Day 1: Containerized FastAPI backend with health endpoint  
- [x] Day 2: Postgres + Alembic migrations; basic data models  
- [x] Day 3: OCR pipeline scaffold (Donut/TrOCR) → parse sample receipts  
- [x] Day 4: Size normalization + unit price calculation  
- [x] Day 5: Web UI scaffold (Next.js) + upload flow  
- [x] Day 6: Alerts logic (shrink & unit-price spike) + tests  
- [x] Day 7: Deploy preview + demo video  

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


## ✅ Day 5 Checkpoint — Frontend Bootstrap (Next.js + Docker)

**What’s live now**

- **Web service scaffolded** (`/web` with Next.js 14)
- **Dockerized frontend** (`docker-compose.yml` now builds & runs `shrinkshield-web` on port **3000**)
- **Global styles** wired (`styles.css`)
- **Basic page (`index.js`)**:
  - Header (`ShrinkShield — Receipts`)
  - File upload control + disabled Upload button
  - Receipt list section
  - Graceful fallback (`"Failed to load receipts"` / `"No receipts yet"`)
- **API integration (GET /receipts)**: frontend fetches receipts from backend
  - currently shows placeholder empty state when no receipts exist
- CORS enabled in backend so browser → API requests work
  
- Endpoints:
  - Backend (API):  
    - `GET /receipts` → list receipts (frontend consumes this)  
    - `POST /receipts` → still curl-only, browser wiring coming next  
  - Frontend (web):  
    - `http://localhost:3000` → renders ShrinkShield UI  

**How to run**
```bash
cd infra
docker compose up --build -d
# logs (optional)
docker compose logs -f web
```

**Visit in browser**
- Open: http://localhost:3000    You should see:
- Page title “ShrinkShield — Receipts”
- File input + Upload button (disabled)
- “Uploaded receipts” section → shows `No receipts yet` if DB is empty


## ✅ Day 6 Checkpoint — Uploads & Alerts Logic

**What’s live now**

- Web UI allows file upload via browser
- Frontend fetches receipts list from backend
- Uploaded receipts are persisted in Postgres
- Receipts list updates immediately on upload
- Backend API endpoints:
  - `POST /receipts` → upload a new receipt
  - `GET /receipts` → list receipts
  - `GET /receipts/{id}` → fetch detailed view

**How to run**

```bash
cd infra
docker compose up --build -d
# logs (optional)
docker compose logs -f backend
docker compose logs -f web
```


## ✅ Day 7 Checkpoint — Deploy Preview & Demo

**What’s live now**

- **Next.js UI** (Dockerized) listing receipts and showing details
  - `GET /receipts` → list with links
  - `GET /receipts/{id}` → raw OCR lines + normalized products with unit price
- **Upload** via UI (stub OCR) persists rows and displays results
- Full stack runs with Docker Compose: `db` (Postgres 16), `backend` (FastAPI), `web` (Next.js)

**How to run (local preview)**

```bash
cd infra
docker compose up --build -d
# logs (optional)
docker compose logs -f web
```
**Open:**

- Web UI: http://localhost:3000
- API: http://localhost:8000
- Health: http://localhost:8000/health
