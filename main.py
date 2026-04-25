import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from core.data import load_data, clean_data
from app.components.map_widget import build_map, CATEGORY_COLORS

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ciudad Visible",
    page_icon="🏙️",
    layout="wide",
)

# ── Data loading ──────────────────────────────────────────────────────────────
# @st.cache_data caches the result so the CSV is only read once per session.
@st.cache_data
def get_data() -> pd.DataFrame:
    df = load_data("data/sample_issues.csv")
    return clean_data(df)


df = get_data()

# ── Sidebar — filters ─────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filtros")

categories = ["Todas"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.selectbox("Categoría", categories)

areas = ["Todas"] + sorted(df["area"].unique().tolist())
selected_area = st.sidebar.selectbox("Zona / Barrio", areas)

statuses = ["Todos"] + sorted(df["status"].unique().tolist())
selected_status = st.sidebar.selectbox("Estado", statuses)

priorities = ["Todas"] + sorted(df["priority"].str.capitalize().unique().tolist())
selected_priority = st.sidebar.selectbox("Prioridad", priorities)

# ── Sidebar — color legend ────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.markdown("**Colores por categoría:**")
EMOJI_FOR_COLOR = {
    "red": "🔴", "orange": "🟠", "green": "🟢", "blue": "🔵",
    "cadetblue": "🔵", "darkred": "🔴", "darkgreen": "🟢",
}
for cat, color in CATEGORY_COLORS.items():
    st.sidebar.markdown(f"{EMOJI_FOR_COLOR.get(color, '⚪')} {cat}")

# ── Apply filters ─────────────────────────────────────────────────────────────
filtered = df.copy()

if selected_category != "Todas":
    filtered = filtered[filtered["category"] == selected_category]
if selected_area != "Todas":
    filtered = filtered[filtered["area"] == selected_area]
if selected_status != "Todos":
    filtered = filtered[filtered["status"] == selected_status]
if selected_priority != "Todas":
    filtered = filtered[filtered["priority"] == selected_priority.lower()]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🏙️ Ciudad Visible")
st.caption("Mapa interactivo de problemas urbanos reportados por la ciudadanía.")

# ── Summary metrics ───────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total reportes", len(filtered))
col2.metric("Abiertos", len(filtered[filtered["status"] == "Abierto"]))
col3.metric("En Proceso", len(filtered[filtered["status"] == "En Proceso"]))
col4.metric("Resueltos", len(filtered[filtered["status"] == "Resuelto"]))

st.markdown("---")

# ── Map ───────────────────────────────────────────────────────────────────────
st.subheader("Mapa de reportes")

if filtered.empty:
    st.warning("No hay reportes para los filtros seleccionados. Prueba otra combinación.")
else:
    m = build_map(filtered)
    # returned_objects=[] prevents Streamlit from re-rendering on every click
    st_folium(m, use_container_width=True, height=500, returned_objects=[])

# ── Charts ────────────────────────────────────────────────────────────────────
st.markdown("---")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Reportes por categoría")
    if not filtered.empty:
        cat_counts = filtered["category"].value_counts().rename_axis("Categoría").reset_index(name="Reportes")
        st.bar_chart(cat_counts.set_index("Categoría"))

with chart_col2:
    st.subheader("Reportes por zona")
    if not filtered.empty:
        area_counts = filtered["area"].value_counts().rename_axis("Zona").reset_index(name="Reportes")
        st.bar_chart(area_counts.set_index("Zona"))

# ── Data table ────────────────────────────────────────────────────────────────
with st.expander("Ver tabla de datos completa"):
    display_cols = ["title", "category", "area", "status", "priority", "date_reported", "description"]
    st.dataframe(
        filtered[display_cols].rename(columns={
            "title": "Título", "category": "Categoría", "area": "Zona",
            "status": "Estado", "priority": "Prioridad",
            "date_reported": "Fecha", "description": "Descripción",
        }),
        use_container_width=True,
        hide_index=True,
    )
