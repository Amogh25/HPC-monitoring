from kafka import KafkaProducer
import json
import random
import psutil
import time
import os

# Define Kafka producer properties
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Define a list of monitored metrics
metrics_list = ['cpu_utilization', 'memory_usage', 'network_traffic', 'disk_usage', 'system_load_average']

# Define a function to generate random metrics data
def generate_metrics_data():
    metrics_data = {}
    for metric in metrics_list:
        if metric == 'cpu_utilization':
            metrics_data[metric] = psutil.cpu_percent(interval=1)
        elif metric == 'memory_usage':
            metrics_data[metric] = psutil.virtual_memory().percent
        elif metric == 'network_traffic':
            metrics_data[metric] = psutil.net_io_counters().bytes_sent
        elif metric == 'disk_usage':
            metrics_data[metric] = psutil.disk_usage('/').percent
        elif metric == 'system_load_average':
            metrics_data[metric] = os.getloadavg()[0]
    return metrics_data

# Generate and send metrics data every second
while True:
    metrics_data = generate_metrics_data()
    producer.send('my-metrics-topic', value=metrics_data)
    producer.flush()
    time.sleep(1)
