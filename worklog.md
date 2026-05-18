# May 18, 2026 12:00:00
Setup python 3.11 version which is compatible with dbt framework.
Explored GA4 dataset and ran few queries

# May 18, 2026, 17:30:00
Exploring & taking required columns fromm the table in GA4 dataset

# May 18, 2026, 19:00:00
Added the raw table after normalising the column, timestamp and data

# May 18, 2026, 20:00:00
Split the raw table events into two intermediate models: all non-purchase events & Completed purchase

# May 19, 2026 00:55:00
Created final attribution tables for first and last click

# May 19, 2026 02:59:00
Completed full dbt pipeline execution (staging -> intermediate -> final models)
Built and validated Streamlit dashboard connected to final attribution models
Confirmed end-to-end data flow from GA4 dataset to final reporting layer
