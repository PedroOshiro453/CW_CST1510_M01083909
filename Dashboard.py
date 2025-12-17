from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
	page_title="Cyber Incidents Dashboard",
	page_icon="🏠",
	layout="wide",
)


DATA_PATH = Path(__file__).parent / "DATA" / "cyber_incidents.csv"


@st.cache_data
def load_cyber_incidents(path: Path) -> pd.DataFrame:
	df = pd.read_csv(path)
	df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
	df = df.dropna(subset=["timestamp"])
	return df.sort_values("timestamp")


data = load_cyber_incidents(DATA_PATH)

st.header("Cyber Incidents Dashboard")
st.write("Welcome to the Home Page of the Application!")

with st.sidebar:
	st.header("Cyber Incidents Overview")
	severity_ = st.selectbox("severity", data["severity"].unique())

filtered_data = data[data["severity"] == severity_]

col1, col2 = st.columns(2)
with col1:
	st.subheader("Number of Incidents by Severity")
	st.bar_chart(filtered_data["category"].value_counts())

with col2:
	st.subheader("Filtered Cyber Incidents Data")
	st.line_chart(filtered_data, x="timestamp", y="incident_id")
	st.dataframe(filtered_data)