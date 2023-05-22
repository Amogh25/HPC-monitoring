from kafka import KafkaProducer
import json
import time

# Define Kafka producer properties
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Define a list of monitored metrics
File_object = open("pcm-alert-kafka.txt","r")
metrics_list = File_object.readlines()
len_list = len(metrics_list)

# Define a function to generate random metrics data
def generate_metrics_data():
    metrics_data = metrics_list[i]
    metrics_data = json.loads(metrics_data)
    return metrics_data
i=0
# Generate and send metrics data every second
while True:
    i=(i+1)%(len_list)
    metrics_data = generate_metrics_data()
    producer.send('metrics1', value=metrics_data)
    producer.flush()
    time.sleep(1)

