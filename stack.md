# Ciudad Visible — Stack & Architecture

## What we're building
A civic-tech platform that maps urban issues in Mexico City and turns scattered
citizen complaints into actionable intelligence for citizens, journalists,
neighborhood groups, and public servants.

---

## Final architecture (target state)

```
ciudad-visible/
│
├── main.py                     # Streamlit entry point (streamlit run main.py)
│
├── app/                        # UI layer — Streamlit only, no business logic
│   ├── components/
│   │   ├── map_widget.py       # Folium map builder
│   │   ├── filters.py          # Sidebar filter widgets
│   │   └── charts.py           # Bar charts, rankings
│   └── pages/                  # Multi-page app (Streamlit native)
│       ├── 01_mapa.py          # Map view (current main.py)
│       ├── 02_tendencias.py    # Trend analysis over time
│       └── 03_reportar.py      # Citizen issue submission form
│
├── core/                       # Business logic — no UI dependency
│   ├── data.py                 # Load + clean data
│   ├── analytics.py            # Trends, critical zones, rankings
│   └── ai/
│       ├── classifier.py       # Free-text → category + priority (Anthropic API)
│       └── summarizer.py       # Weekly summaries
│
├── db/                         # Database layer
│   ├── models.py               # SQLAlchemy table definitions
│   ├── queries.py              # Named queries (get_issues, filter_by_zone…)
│   └── schema.sql
│
├── pipelines/                  # Offline ingestion scripts
│   ├── ingest_cdmx.py          # Pull from datos.cdmx.gob.mx
│   └── seed.py                 # Load sample CSV → DB for local dev
│
├── api/                        # FastAPI — only when external access is needed
│   ├── main.py
│   ├── routes/
│   │   ├── issues.py
│   │   └── analytics.py
│   └── schemas/
│       └── issue.py
│
├── data/
│   ├── raw/                    # Downloaded source files, never edited
│   ├── processed/              # Clean files ready to load
│   └── sample_issues.csv       # Placeholder (Medellín coords → replace with CDMX)
│
├── tests/
├── .env.example
├── .gitignore
├── CLAUDE.md
├── requirements.txt
└── stack.md
```

---

## Tech stack

| Layer       | Tool                          | Status     |
|-------------|-------------------------------|------------|
| UI          | Streamlit                     | Active     |
| Data        | Pandas                        | Active     |
| Maps        | Folium + streamlit-folium     | Active     |
| Spatial     | GeoPandas                     | Planned    |
| Database    | SQLite → PostgreSQL           | Planned    |
| Backend API | FastAPI                       | Future     |
| AI          | Anthropic API (Claude)        | Planned    |
| Hosting     | Streamlit Cloud / Vercel      | Future     |

---

## Phases

### V1 — Local MVP (done)
- Streamlit app reads a CSV of synthetic issues
- Interactive Folium map with filters by category, zone, status, priority
- Summary metrics and bar charts

### V2 — Real data + database
- Replace CSV with real CDMX open data (datos.cdmx.gob.mx)
- Add SQLite database with SQLAlchemy
- Write `pipelines/ingest_cdmx.py` to pull and clean real complaints
- Add `core/analytics.py`: trend over time, critical zones ranking

### V3 — AI features
- Add `core/ai/classifier.py`: classify free-text complaints into category + priority
- Add citizen submission form (`app/pages/03_reportar.py`)
- Add `core/ai/summarizer.py`: weekly summaries per zone

### V4 — Public platform
- Add FastAPI backend for external access / future mobile app
- Multi-page Streamlit app with dedicated views (trends, submission, rankings)
- Public dashboard with shareable links

---

## How we start each session

1. `streamlit run main.py` — verify the app runs
2. Work only on the current phase (V2 right now)
3. Business logic goes in `core/`, UI goes in `app/`, never mix them
4. Test manually in the browser before pushing
