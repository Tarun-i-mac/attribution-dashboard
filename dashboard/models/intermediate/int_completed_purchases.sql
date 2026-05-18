SELECT *
FROM {{ ref('stg_user_journey_events') }}
WHERE event_name = 'purchase'
and purchase_revenue IS NOT NULL