from kafka import KafkaProducer
import json
from time import sleep
import random

# Define Kafka producer properties
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Define a list of monitored metrics
with open("pcm-alert-kafka.txt", "r") as f:
    metrics_list = [json.loads(line) for line in f]

# Define a function to generate random metrics data
def generate_metrics_data():
    return random.choice(metrics_list)

def size_simulation():
    time_delay = 5.0
    while True:
        metrics_data = generate_metrics_data()
        if random.uniform(1, 10) <= 5:
            metrics_data= str(metrics_data)* 5
        producer.send('tests2', value=metrics_data)
        producer.flush()
        sleep(time_delay)

def frequency_simulation():
    time_delay = 5.0
    while True:
        metrics_data = generate_metrics_data()
        if random.uniform(1, 10) <= 5:
            time_delay = 1.0
        producer.send('tests2', value=metrics_data)
        producer.flush()
        sleep(time_delay)

def latency_simulation():
    time_delay = 5.0
    while True:
        metrics_data = generate_metrics_data()
        if random.uniform(1, 10) <= 5:
            sleep(5)
        producer.send('tests2', value=metrics_data)
        producer.flush()
        sleep(time_delay)

# Choose simulation
choices = [1, 2, 3]
choice = int(input("Enter simulation type: "))
if choice == 1:
    size_simulation()
elif choice == 2:
    latency_simulation()
elif choice == 3:
    frequency_simulation()
