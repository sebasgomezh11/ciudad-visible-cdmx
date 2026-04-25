import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """Read the CSV file and return a raw DataFrame."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and normalize the raw DataFrame.

    Rules applied:
    - Rows without lat/lon coordinates are dropped (can't be mapped).
    - date_reported is parsed to datetime; unparseable values become NaT.
    - Text columns (category, area, status) are trimmed and title-cased for
      consistent filtering (e.g. "en proceso" → "En Proceso").
    - priority is lowercased for consistent comparisons.
    """
    # Must have coordinates to appear on the map
    df = df.dropna(subset=["latitude", "longitude"]).copy()

    df["date_reported"] = pd.to_datetime(df["date_reported"], errors="coerce")

    for col in ["category", "area", "status"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    df["priority"] = df["priority"].astype(str).str.strip().str.lower()

    return df.reset_index(drop=True)
