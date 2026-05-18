SELECT
  user_pseudo_id,
  event_timestamp AS raw_event_timestamp,
  CAST(TIMESTAMP_MICROS(event_timestamp) AS TIMESTAMP) AS event_ts,
  CAST(TIMESTAMP_MICROS(event_timestamp) AS DATE) AS event_date,
  event_name,
  traffic_source.source AS source,
  traffic_source.medium AS medium,
  traffic_source.name AS campaign,

  CASE
    WHEN traffic_source.medium IS NULL THEN 'Direct'
    WHEN traffic_source.medium = '(none)' THEN 'Direct'
    WHEN traffic_source.medium = 'organic' THEN 'Organic Search'
    WHEN traffic_source.medium = 'cpc' THEN 'Paid Search'
    WHEN traffic_source.medium = 'referral' THEN 'Referral'
    WHEN traffic_source.medium = '<Other>' THEN 'Other'
    WHEN traffic_source.medium = '(data deleted)' THEN 'Unknown'
    ELSE INITCAP(traffic_source.medium)
  END AS channel,

  ecommerce.purchase_revenue AS purchase_revenue

FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20210101' AND '20210131'