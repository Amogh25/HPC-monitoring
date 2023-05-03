from kafka import KafkaProducer, KafkaConsumer
import json
from time import sleep
import random
import argparse

# Parse the command line arguments
parser = argparse.ArgumentParser(description='Simulate metrics data and send to Kafka topic.')
parser.add_argument('file', type=str, help='Name of the file containing the list of monitored metrics')
args = parser.parse_args()
# Extract the topic name from the file name
topic_name = args.file.split('.')[0]

# Define Kafka producer properties
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Define a list of monitored metrics
with open(args.file, "r") as f:
    metrics_list = [json.loads(line) for line in f]

with open('topiclist.txt', 'a') as f:
    f.write(topic_name + '\n')

# Define a function to generate random metrics data
length=len(metrics_list)

def frequency_simulation():
    i=-1   
    time_delay = 5.0
    while True:
        i=(i+1)%length
        metrics_data = metrics_list[i]
        if random.uniform(1, 10) <= 3:
            time_delay = 1
        producer.send(topic_name, value=metrics_data)
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
        producer.send(topic_name, value=metrics_data)
        producer.flush()
        sleep(time_delay)

# Choose simulation
choices = [1, 2]
choice = random.choice(choices)
if choice == 1:
    latency_simulation()
elif choice == 2:
    frequency_simulation()
