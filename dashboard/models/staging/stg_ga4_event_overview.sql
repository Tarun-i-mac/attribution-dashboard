select
    event_name,
    count(*) as total_events
from `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
where _table_suffix between '20210120' and '20210131'
group by event_name
order by total_events desc
limit 20