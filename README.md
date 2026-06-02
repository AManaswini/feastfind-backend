# FeastFind Backend — FastAPI

AI-powered catering marketplace API. Python 3.11+ · FastAPI · Anthropic Claude.

## Folder Structure

```
feastfind-backend/
├── app/
│   ├── main.py                   # FastAPI app, CORS, router registration
│   ├── core/
│   │   └── config.py             # Pydantic settings — reads .env
│   ├── data/
│   │   └── seed.py               # Dummy caterer + inquiry data
│   ├── models/
│   │   └── matcher.py            # Keyword-based caterer scoring engine
│   ├── routers/
│   │   ├── caterers.py           # GET /api/caterers, GET /api/caterers/{id}
│   │   ├── inquiries.py          # POST /api/inquiries
│   │   ├── chat.py               # POST /api/chat  (Claude proxy + matcher)
│   │   └── events.py             # GET /api/events/types
│   └── schemas/
│       └── caterer.py            # Pydantic request/response models
├── tests/
│   └── test_caterers.py          # pytest test suite
├── .env.example
├── requirements.txt
└── README.md
```

## Quick Start

```bash
cd feastfind-backend

# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| GET    | /                         | Health check                             |
| GET    | /health                   | Health check (JSON)                      |
| GET    | /api/caterers             | List all caterers (filterable)           |
| GET    | /api/caterers/{id}        | Get caterer detail                       |
| POST   | /api/inquiries            | Submit a caterer inquiry                 |
| GET    | /api/inquiries            | List all inquiries (admin)               |
| POST   | /api/chat                 | AI chat with Claude + auto-matching      |
| GET    | /api/events/types         | List supported event types               |

### Query params for GET /api/caterers
- `cuisine` — filter by cuisine string (e.g. `Telugu`)
- `verified` — `true` / `false`
- `min_rating` — float (e.g. `4.5`)
- `location` — city string (e.g. `San Jose`)

## Connecting the React Frontend

Update `src/hooks/useAIChat.js` to call your backend instead of Anthropic directly:

```js
// Before (direct browser call):
const response = await fetch('https://api.anthropic.com/v1/messages', { ... })

// After (via backend):
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ messages }),
});
const data = await response.json();
// data.reply         — assistant text
// data.extracted_info — parsed event details
// data.recommendations — ranked caterers
```

## Running Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

## Upgrading to Production

| Feature             | Current (dummy)      | Production                        |
|---------------------|----------------------|-----------------------------------|
| Data storage        | In-memory list       | PostgreSQL via SQLAlchemy         |
| Caterer matching    | Keyword scoring      | pgvector cosine similarity        |
| Auth                | None                 | JWT (fastapi-users)               |
| Email notifications | TODO comment         | SendGrid / Resend                 |
| File uploads        | Not implemented      | S3 / Cloudflare R2                |
| Deployment          | uvicorn local        | Docker → Railway / Render / AWS   |
