from kafka import KafkaProducer, KafkaConsumer
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
length=len(metrics_list)


def size_simulation():
    i=-1
    
    time_delay = 5.0
    while True:
        i=(i+1)%length
        metrics_data = metrics_list[i]
        if random.uniform(1, 10) <= 3:
            metrics_data *= 15
        producer.send('tests2', value=metrics_data)
        producer.flush()
        sleep(time_delay)

def frequency_simulation():
    i=-1   
    time_delay = 5.0
    while True:
        i=(i+1)%length
        metrics_data = metrics_list[i]
        if random.uniform(1, 10) <= 3:
            time_delay = 1
        producer.send('tests2', value=metrics_data)
        producer.flush()
        sleep(time_delay)

def latency_simulation():
    i=-1
    time_delay = 15.0
    while True:
        i=(i+1)%length
        metrics_data = metrics_list[i]
        if random.uniform(1, 10) <= 3:
            sleep(5)
        producer.send('tests2', value=metrics_data)
        producer.flush()
        sleep(time_delay)

# Choose simulation
choices = [1, 2, 3]
choice = random.choice(choices)
if choice == 1:
    size_simulation()
elif choice == 2:
    latency_simulation()
elif choice == 3:
    frequency_simulation()
