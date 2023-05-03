from kafka import KafkaConsumer
from prometheus_client import start_http_server, Gauge
from threading import Thread
import argparse

# Create argument parser object
parser = argparse.ArgumentParser()

# Add arguments for value_field and topic_field
parser.add_argument('--value_field', help='name of field containing value', required=True)
#parser.add_argument('--separator_field', help='name of field containing separator', required=True)

# Parse the command line arguments
args = parser.parse_args()

# Get the value of value_field and topic_field from the parsed arguments
value_field = args.value_field
#separator_field = args.seperator_field

# create a gauge metric with topics
g = Gauge(value_field, 'My gauge description', ['topic'])

# function to consume messages from Kafka topic and update the metric for each mode
def consume_messages(consumer, topic):   
    for message in consumer:
        # convert the message value to a dictionary
        data = eval(message.value)
        
        # extract the topic and value from the dictionary
        value = data[value_field]
        #separator = data[separator_field]
        
        # set the gauge value for the topic
        g.labels(topic).set(value)

# read topics from input file
with open('topiclist.txt', 'r') as f:
    topics = [t.strip() for t in f.readlines()]

# create a Kafka consumer instance for each topic and start a separate thread for each consumer
for topic in topics:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],  # replace with the Kafka broker addresses
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='my-group'
    )
    t = Thread(target=consume_messages, args=(consumer, topic))
    t.start()

# start the Prometheus HTTP server
start_http_server(8080)  # replace with the desired port number


# 
# python my_script.py --value_field my_value_field
