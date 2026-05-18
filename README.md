# attribution-dashboard
This project builds a simple end-to-end attribution pipeline using GA4 event data in BigQuery. The goal is to compute **first-click and last-click attribution models**, and visualize revenue performance through an interactive dashboard.

---

# Attribution Assumptions
1. Uses user_pseudo_id instead of user_id because of the null values present in user_id column.
2. Using 30 days as my lookback window.
3. First click - Earliest click within my lookback duration'
4. latst click - Before the purchase.
5. tie-breakers - If two events have the same timestamp, we break ties using event_id.

---

## Architecture
GA4 Public Dataset
↓
stg_user_journey_events
↓
int_customer_touchpoints
↓
int_completed_purchases
↓
first_click_attribution
last_click_attribution
↓
Streamlit Dashboard

---

## Tech Stack

- BigQuery (data warehouse)
- dbt (data modeling)
- Python (orchestration + dashboard)
- Streamlit (UI layer)
- Plotly (visualization)

---

## Data Source

- Google Analytics 4 public dataset in BigQuery:
  `bigquery-public-data.ga4_obfuscated_sample_ecommerce`

---

## Models Breakdown

### Staging Layer
- `stg_user_journey_events`
- `stg_ga4_event_overview`

These models standardize raw GA4 events and extract key fields:
- user_pseudo_id
- event timestamp
- traffic source
- channel mapping

---

### Intermediate Layer
- `int_customer_touchpoints`
- `int_completed_purchases`

These models:
- separate purchase and non purchase events
- prepare clean user journey sequences
- structure data for attribution logic

---

### Final Layer (Attribution Models)

#### First Click Attribution
Assigns conversion credit to the **first interaction** in a user journey.

#### Last Click Attribution
Assigns conversion credit to the **last interaction before purchase**.

Both models are built using window functions over:
- `user_pseudo_id`
- `event_ts`

---

## Key Assumptions

- User identity is based on `user_pseudo_id`
- A purchase event represents a conversion point
- Attribution is calculated at a user + event level
- In case of duplicate timestamps, ordering is resolved using event sequencing logic

---

## Lookback Window

- Based on GA4 sample dataset availability
- Last 14 days of `purchase_time` used for trend analysis

---

## Dashboard Features

- Total First Click Revenue
- Total Last Click Revenue
- 14-day revenue trend
- Channel wise revenue breakdown
- Live view of recent events

--- 
## Run Instructions
1. Install dependencies
```bash
   pip install -r requirements.txt
```

2. Run dbt pipeline
   dbt run

Run tests:

    dbt test

Inspect models:

    dbt ls

Run specific model:

   dbt run --select stg_user_journey_events

3. Run Streamlit dashboard
python -m streamlit run dashboard/app.py

--- 
## Failure Handling
- dbt failures
- Ensure staging models exist before intermediate models
- Validate dataset path: labs.*
- Ensure correct schema mapping (event_ts, purchase_time)

# Monitoring Suggestions
- dbt run logs
- Model execution time tracking
- Data quality monitoring (dbt tests)

- Revenue drift by channel
- First vs Last click gap tracking

- not_null checks on:
user_pseudo_id
event_ts
purchase_time



# Cost Notes
- Uses GA4 sample dataset (limited time window)
- Only required columns selected in staging
- dbt models materialized as views (low cost)
- No heavy runtime aggregations in dashboard


