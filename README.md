# attribution-dashboard


# Attribution Assumptions
1. Uses user_pseudo_id instead of user_id because of the null values present in user_id column.
2. Using 30 days as my lookback window.
3. First click - Earliest click within my lookback duration'
4. latst click - Before the purchase.
5. tie-breakers - if 2 points had the same timestamp, Will use event_name as my tie breaker.
