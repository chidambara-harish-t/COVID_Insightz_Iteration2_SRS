import streamlit as st
import pandas as pd
from src.load import get_data
from src.transform import summary_stats, global_cases, format_region
from src.viz import plot_daily, plot_global, plot_top10
from src.config import DEFAULT_COUNTRIES

# Streamlit page config
st.set_page_config(page_title="COVID Insights", layout="wide")

df = get_data()
df = global_cases(df)

# Sidebar  labels
labels_map = {format_region(col): col for col in df.columns if col[0] not in ["Date", "GlobalCases"]}

st.sidebar.header("Available countries:")
from src.config import DEFAULT_COUNTRIES

# Sidebar labels
labels_map = {format_region(col): col for col in df.columns if col[0] not in ["Date", "GlobalCases"]}

st.sidebar.header("Available countries:")

# Default comes from config.py
default_labels = [c for c in DEFAULT_COUNTRIES if c in labels_map]

countries_labels = st.sidebar.multiselect(
    "Select countries to view",
    list(labels_map.keys()),
    default=default_labels
)

# Map back to original column names 
countries = [labels_map[l] for l in countries_labels]

# Date filter
min_date, max_date = df[("Date", "")].min(), df[("Date", "")].max()
date_range = st.sidebar.date_input(
    "Select date range:",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter dataframe by date range
if len(date_range) == 2:
    start_date, end_date = date_range
    df = df[(df[("Date", "")] >= pd.to_datetime(start_date)) & (df[("Date", "")] <= pd.to_datetime(end_date))]

# Landing Page
st.title("COVID-19 Insights Dashboard")
st.markdown("### This dashboard provides insights into COVID-19 trends by country and globally.")

# latest totals per country/province
latest = df.iloc[-1].drop(labels=[("Date", ""), ("GlobalCases", "")], errors="ignore")
latest = pd.to_numeric(latest, errors="coerce").dropna()

st.subheader("Top 10 Countries by Total Cases (Latest Day)")
fig_top10 = plot_top10(latest)
st.pyplot(fig_top10)

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Daily Trend", "📊 Summary Stats", "🌍 Global Trend"])

with tab1:
    st.subheader("Daily COVID-19 Confirmed Cases by Country")
    if countries:
        fig = plot_daily(df, countries)
        st.pyplot(fig)

with tab2:
    st.subheader("Summary Stats for Selected Countries")
    if countries:
        stats = summary_stats(df, countries)
        st.table(stats)

        # CSV download
        csv = stats.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Summary Stats as CSV", csv, "summary_stats.csv", "text/csv")

with tab3:
    st.subheader("Global COVID-19 Confirmed Cases Over Time")
    fig2 = plot_global(df)
    st.pyplot(fig2)

    # CSV download
    csv_all = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data as CSV", csv_all, "filtered_data.csv", "text/csv")
    st.markdown("Data source: [JHU CSSE COVID-19 Data](https://www.kaggle.com/datasets/antgoldbloom/covid19-data-from-john-hopkins-university)")