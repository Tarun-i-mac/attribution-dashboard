import streamlit as st
from google.cloud import bigquery
import plotly.express as px
import pandas as pd
from datetime import datetime

# Setup

st.set_page_config(
    page_title="Attribution Dashboard",
    layout="wide"
)

st.title("Attribution Dashboard")

client = bigquery.Client(project="project-92d8b8b8-6c6a-463a-88d")

PROJECT = "project-92d8b8b8-6c6a-463a-88d"
DATASET = "labs"

# Data loaders

@st.cache_data(ttl=300)
def load_first_click():
    return client.query(f"""
        SELECT *
        FROM `{PROJECT}.{DATASET}.first_click_attribution`
    """).to_dataframe()


@st.cache_data(ttl=300)
def load_last_click():
    return client.query(f"""
        SELECT *
        FROM `{PROJECT}.{DATASET}.last_click_attribution`
    """).to_dataframe()


@st.cache_data(ttl=60)
def load_stream_events():
    return client.query(f"""
        SELECT
            event_ts,
            user_pseudo_id,
            event_name,
            source,
            medium,
            campaign
        FROM `{PROJECT}.{DATASET}.raw_stream_events`
        ORDER BY event_ts DESC
        LIMIT 50
    """).to_dataframe()


@st.cache_data(ttl=300)
def load_trend():
    return client.query(f"""
        SELECT
            DATE(purchase_time) AS event_date,
            SUM(purchase_revenue) AS revenue
        FROM `{PROJECT}.{DATASET}.last_click_attribution`
        WHERE DATE(purchase_time) >= DATE_SUB(DATE '2021-01-31', INTERVAL 14 DAY)
        GROUP BY event_date
        ORDER BY event_date
    """).to_dataframe()

# Load data

first_df = load_first_click()
last_df = load_last_click()
stream_df = load_stream_events()
trend_df = load_trend()

# KPIs

fc_rev = first_df["purchase_revenue"].sum()
lc_rev = last_df["purchase_revenue"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("First Click Revenue", f"{fc_rev:,.0f}")

with col2:
    st.metric("Last Click Revenue", f"{lc_rev:,.0f}")

st.markdown("---")

# 14-day trend

st.subheader("14-day Revenue Trend")

fig = px.line(
    trend_df,
    x="event_date",
    y="revenue",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Channel breakdown

st.subheader("Channel Breakdown (Last Click)")

channel_df = (
    last_df.groupby("channel", as_index=False)["purchase_revenue"]
    .sum()
    .sort_values("purchase_revenue", ascending=False)
)

fig2 = px.bar(
    channel_df,
    x="channel",
    y="purchase_revenue"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Live events

st.subheader("Recent Events (Stream)")

st.dataframe(stream_df, use_container_width=True)

# Refresh

if st.button("Refresh"):
    st.rerun()