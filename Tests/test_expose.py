from prometheus_client import start_http_server, Summary, Gauge
import time
import pandas as pd
import os

#Read Test CSV and get column of data
csv_path = os.path.dirname(os.path.abspath(__file__)) + "\\sample_data.csv"
df = pd.read_csv(csv_path)
saved_column = df.Data

#Initialize PG Mono Gauge
g = Gauge('Test_PG',unit='Torr',documentation="Readings from PG Mono")
"""
print(saved_column)
for i in saved_column:
    print(i)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):

    time.sleep(t)
"""

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)

    #set Gauge data to current "reading" every 10 seconds forever, cycling through the file over and over.
    while True:
        for i in saved_column:
            time.sleep(10)
            print(i)
            g.set(i)

