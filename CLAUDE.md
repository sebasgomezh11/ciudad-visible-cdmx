# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

**Ciudad Visible** (working title) — a civic-tech platform that maps urban issues in **Mexico City** and turns scattered citizen complaints into actionable patterns. Built solo, low budget, fast iteration.

**Mission:** Use data and AI to make urban problems visible and help citizens make better decisions.

**Target users:** Citizens, neighborhood groups, journalists, urbanists, public servants, researchers.

**Current state (V1 MVP):** Interactive map with filters on synthetic sample data.

**Planned MVP features not yet built:**
- Trend analysis over time
- AI classification of free-text complaints (Anthropic API preferred; OpenAI optional)
- Weekly summaries
- Critical zones ranking

**Planned stack additions:** GeoPandas (spatial analysis), SQL (when data grows beyond CSV), possibly a free-text intake form with AI classification.

**Constraints that affect code decisions:** Solo builder, low budget — avoid overengineering, prefer simple solutions, keep dependencies minimal, favor fast iteration over abstraction.

> Note: `data/sample_issues.csv` uses synthetic Medellín, Colombia data as a placeholder. Real data will be Mexico City (CDMX). Future sample data should use CDMX coordinates and alcaldías (Cuauhtémoc, Benito Juárez, Coyoacán, etc.) as the `area` field.

## Running the app

```bash
# Install dependencies (first time or after requirements.txt changes)
pip install -r requirements.txt

# Start the app — opens http://localhost:8501
streamlit run app.py
```

Always run from the repo root. `load_data` uses a relative path (`data/sample_issues.csv`) that resolves from wherever `streamlit run` is invoked.

## Architecture

The app has three layers that execute in order on every Streamlit rerun:

1. **Data** (`utils/data_loader.py`) — `load_data()` reads the CSV; `clean_data()` normalizes it. Text columns (`category`, `area`, `status`) are title-cased so filter comparisons always match. `priority` is lowercased. Rows missing lat/lon are dropped. The result is cached via `@st.cache_data` in `app.py`.

2. **Filtering** (`app.py`) — Four sidebar widgets (category, area, status, priority) reduce the cached DataFrame into a `filtered` subset. All downstream rendering works on `filtered`, never the raw `df`.

3. **Rendering** (`utils/map_builder.py` + `app.py`) — `build_map(filtered)` iterates the filtered DataFrame and adds a `folium.CircleMarker` per row, colored by `CATEGORY_COLORS`. The map is embedded via `st_folium(..., returned_objects=[])` — the empty list is intentional and prevents Streamlit from re-rendering on map clicks.

## Data schema

`data/sample_issues.csv` columns: `id`, `title`, `category`, `area`, `latitude`, `longitude`, `status`, `date_reported`, `priority`, `description`

- `category` values: `Agua`, `Alumbrado`, `Basuras`, `Espacios Verdes`, `Infraestructura`, `Seguridad`, `Vías`
- `status` values: `Abierto`, `En Proceso`, `Resuelto`
- `priority` values (lowercase): `alta`, `media`, `baja`

When adding a new category, also add its color to `CATEGORY_COLORS` in `utils/map_builder.py` — otherwise its markers render gray and it won't appear in the sidebar legend.

## Key constraints

- **`@st.cache_data`** — `get_data()` is only called once per session. If you change the CSV or cleaning logic during development, call `st.cache_data.clear()` or restart the server.
- **`returned_objects=[]`** on `st_folium` — do not remove this; it suppresses unnecessary reruns triggered by map interaction events.
- **Title-case normalization** — filter comparisons in `app.py` (`== "Abierto"`, `== "En Proceso"`) depend on `clean_data()` having title-cased the `status` column. Keep them consistent.

## How we work

**User background:** Analytics and strategy. Improving technical skills while building real projects. Not a beginner — explain like a smart builder, not a tutorial.

**What they need:** Product thinking, Python implementation, data pipelines, AI use cases, architecture decisions, UX ideas, prioritization, shipping fast.

**Style:** Clear and direct. Practical over academic. Challenge assumptions. Give next actions. Never just answer a question — help move the project forward.

**Default response format for questions and decisions:**
1. Recommendation
2. Why
3. How to execute
4. Risks
5. Next step
