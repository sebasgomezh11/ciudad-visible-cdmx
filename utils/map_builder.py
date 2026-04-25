import folium
import pandas as pd

# One color per category — keeps the map readable at a glance.
CATEGORY_COLORS: dict[str, str] = {
    "Infraestructura": "red",
    "Alumbrado": "orange",
    "Basuras": "green",
    "Vías": "blue",
    "Agua": "cadetblue",
    "Seguridad": "darkred",
    "Espacios Verdes": "darkgreen",
}


def build_map(df: pd.DataFrame) -> folium.Map:
    """
    Create a Folium map centered on the data's average coordinates.
    Each row becomes a CircleMarker with a clickable popup.
    """
    center = [df["latitude"].mean(), df["longitude"].mean()]
    m = folium.Map(location=center, zoom_start=13, tiles="CartoDB positron")

    for _, row in df.iterrows():
        color = CATEGORY_COLORS.get(row["category"], "gray")

        date_str = (
            row["date_reported"].strftime("%Y-%m-%d")
            if pd.notna(row["date_reported"])
            else "N/A"
        )

        popup_html = f"""
            <div style="font-family: sans-serif; min-width: 180px;">
                <b>{row['title']}</b><br><br>
                <b>Categoría:</b> {row['category']}<br>
                <b>Zona:</b> {row['area']}<br>
                <b>Estado:</b> {row['status']}<br>
                <b>Prioridad:</b> {row['priority'].capitalize()}<br>
                <b>Fecha:</b> {date_str}<br><br>
                <i>{row['description']}</i>
            </div>
        """

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=9,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=row["title"],
        ).add_to(m)

    return m
