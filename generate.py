import os
from datetime import datetime, timedelta

# List of filenames from your screenshot
filenames = [
    "Management.txt",
    "cache-size.txt",
    "cache-usage.txt",
    "flashjournal.txt",
    "memory-status.txt",
    "network-health-detail.txt",
    "network-health.txt",
    "nodes.txt",
    "persistence-detail.txt",
    "persistence.txt",
    "ramjournal.txt",
    "report-cache-storage.txt",
    "report-proxy-connections.txt",
    "report-proxy.txt",
    "service-partitions.txt",
    "service.txt"
]

# Base time is now
now = datetime.now()

# Loop over the last 3 days, hour by hour
for days_ago in range(3):
    for hour in range(24):
        timestamp = (now - timedelta(days=days_ago, hours=now.hour - hour))
        time_str = timestamp.strftime('%Y%m%d%H')
        for name in filenames:
            new_filename = f"{time_str}-{name}"
            with open(new_filename, "w") as f:
                f.write(f"Dummy content for {new_filename}\n")
