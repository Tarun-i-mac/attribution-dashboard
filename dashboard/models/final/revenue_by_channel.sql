SELECT
  channel,
  SUM(purchase_revenue) AS total_revenue,
  COUNT(*) AS total_purchases
FROM {{ ref('first_click_attribution') }}
GROUP BY channel
ORDER BY total_revenue DESC