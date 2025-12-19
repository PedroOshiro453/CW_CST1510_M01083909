from __future__ import annotations

from pathlib import Path
import pandas as pd
import streamlit as st


# --------------------------------------------------
# Paths (always relative to this file)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA"
CSV_PATH = DATA_DIR / "cyber_incidents.csv"


# --------------------------------------------------
# Data loading
# --------------------------------------------------
def load_cyber_incidents() -> pd.DataFrame:
    """
    Load cyber incidents from CSV.

    Expected columns:
    incident_id,timestamp,severity,category,status,description

    Important:
    - The provided dataset may contain time-only timestamps (e.g. '00:00.0').
      For plotting, we may generate a synthetic timeline to match the expected layout.
    """
    if not CSV_PATH.exists():
        st.error("DATA/cyber_incidents.csv not found.")
        st.stop()

    df = pd.read_csv(CSV_PATH)

    # Ensure expected columns exist
    expected = ["incident_id", "timestamp", "severity", "category", "status", "description"]
    for col in expected:
        if col not in df.columns:
            df[col] = ""

    # incident_id -> int
    df["incident_id"] = pd.to_numeric(df["incident_id"], errors="coerce").fillna(0).astype(int)

    # timestamp -> datetime (best effort)
    ts = pd.to_datetime(df["timestamp"], errors="coerce")

    # If most timestamps fail, try parsing time-only like "00:00.0"
    if ts.isna().mean() > 0.5:
        t = pd.to_datetime(
            df["timestamp"].astype(str).str.strip(),
            format="%H:%M.%f",
            errors="coerce",
        )
        # attach a dummy date so it becomes datetime
        dummy_date = pd.Timestamp("2025-01-01")
        ts = dummy_date + (t - t.dt.normalize())

    df["timestamp"] = ts

    # Drop only completely unusable timestamps
    df = df.dropna(subset=["timestamp"])

    # Sort by incident_id for consistent order
    df = df.sort_values("incident_id").reset_index(drop=True)

    return df


def build_plot_timeline(df: pd.DataFrame) -> pd.Series:
    """
    Build a plot-friendly datetime index.

    If the dataset timestamps do not vary enough (e.g., many '00:00.0'),
    we create a synthetic timeline so the chart shows a meaningful line,
    similar to the reference dashboard image.

    Returns a pd.Series of datetimes with the same length as df.
    """
    # How many unique timestamps do we actually have?
    unique_ts = df["timestamp"].nunique(dropna=True)
    n = len(df)

    # If timestamps have low uniqueness, create synthetic timestamps
    # Example: n=200, unique_ts=1 -> synthetic timeline needed
    if unique_ts <= max(3, n // 10):
        base = pd.Timestamp("2025-01-01 00:00:00")
        # Increment by minutes to generate distinct x-axis labels
        synthetic = base + pd.to_timedelta(range(n), unit="min")
        return pd.Series(synthetic, index=df.index)

    # Otherwise, use the real timestamp column
    return df["timestamp"]


# --------------------------------------------------
# Page rendering
# --------------------------------------------------
def render_cyber_incidents_page() -> None:
    st.header("Cyber Incidents Dashboard")
    st.write("Welcome to the Home Page of the Application!")

    data = load_cyber_incidents()

    # Sidebar filter
    with st.sidebar:
        st.header("Cyber Incidents Overview")
        severity_ = st.selectbox("severity", sorted(data["severity"].dropna().unique()))

    filtered = data[data["severity"] == severity_].copy()

    # Charts
    col1, col2 = st.columns(2)

    # Left chart: counts by category (matches reference)
    with col1:
        st.subheader("Number of Incidents by Severity")
        st.bar_chart(filtered["category"].value_counts())

    # Right chart: incident_id over time (matches reference intent)
    with col2:
        st.subheader("Filtered Cyber Incidents Data")

        if filtered.empty:
            st.info("No records for the selected severity.")
        else:
            # Build a timeline that actually varies on the x-axis
            filtered = filtered.sort_values("incident_id").reset_index(drop=True)
            filtered["plot_timestamp"] = build_plot_timeline(filtered)

            # If multiple points share the same timestamp, aggregate incident_id (mean)
            # This prevents duplicate-index issues.
            line_df = (
                filtered.groupby("plot_timestamp", as_index=True)["incident_id"]
                .mean()
                .to_frame()
            )

            # Streamlit line chart expects index = x-axis
            st.line_chart(line_df)

    # Table
    st.write("---")
    st.subheader("Filtered Cyber Incidents Table")
    st.dataframe(
        filtered[["incident_id", "timestamp", "severity", "category", "status", "description"]],
        use_container_width=True,
        hide_index=True,
    )
