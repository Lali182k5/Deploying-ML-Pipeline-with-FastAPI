import pandas as pd

ORDERS = pd.DataFrame(
    [
        {
            "order_id": 1,
            "customer_id": 101,
            "order_date": "2024-11-01",
            "status": "shipped",
            "amount": 120.5,
            "channel": "web",
        },
        {
            "order_id": 2,
            "customer_id": 102,
            "order_date": "2024-11-02",
            "status": "processing",
            "amount": 90.2,
            "channel": "store",
        },
        {
            "order_id": 3,
            "customer_id": 101,
            "order_date": "2024-11-10",
            "status": "shipped",
            "amount": 300.0,
            "channel": "web",
        },
    ]
)

CUSTOMERS = pd.DataFrame(
    [
        {"customer_id": 101, "segment": "SMB", "country": "US", "created_at": "2023-01-01"},
        {"customer_id": 102, "segment": "ENT", "country": "UK", "created_at": "2023-04-10"},
    ]
)

