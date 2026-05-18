WITH base AS (
  SELECT
    p.user_pseudo_id,
    p.event_ts AS purchase_time,
    p.purchase_revenue,
    t.event_ts AS touchpoint_time,
    t.channel,
    t.source,
    t.medium,
    t.campaign,
    ROW_NUMBER() OVER (
      PARTITION BY p.user_pseudo_id, p.event_ts
      ORDER BY t.event_ts DESC
    ) AS rn
  FROM `project-92d8b8b8-6c6a-463a-88d.labs.int_completed_purchases` p
  JOIN `project-92d8b8b8-6c6a-463a-88d.labs.int_customer_touchpoints` t
    ON p.user_pseudo_id = t.user_pseudo_id
   AND t.event_ts <= p.event_ts
)

SELECT *
FROM base
WHERE rn = 1