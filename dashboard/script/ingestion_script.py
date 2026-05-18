from google.cloud import bigquery
import pandas as pd
from datetime import datetime
import uuid
import random
import time

client = bigquery.Client()

table_id = "project-92d8b8b8-6c6a-463a-88d.labs.raw_stream_events"

sources = ["google", "facebook", "direct", "newsletter"]
mediums = ["organic", "cpc", "referral", "(none)"]
campaigns = ["summer_sale", "brand_awareness", "retargeting", "none"]

rows = []

# simulate streaming in small batches
for batch in range(2):  # 2 batches = "streaming simulation"
    
    batch_rows = []
    
    for i in range(5):  # 5 events per batch
        batch_rows.append({
            "user_pseudo_id": f"user_{random.randint(1,5)}",
            "event_ts": datetime.utcnow(),
            "event_name": random.choice(["page_view", "add_to_cart", "purchase"]),
            "source": random.choice(sources),
            "medium": random.choice(mediums),
            "campaign": random.choice(campaigns),
            "event_id": str(uuid.uuid4())
        })

    df = pd.DataFrame(batch_rows)
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # wait for completion

    print(f"Batch {batch + 1} loaded successfully with {len(df)} rows")

    # simulate delay like real streaming
    time.sleep(3)

print("Pseudo-streaming completed successfully")