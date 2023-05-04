from kafka import KafkaConsumer
from prometheus_client import start_http_server, Gauge
import argparse
from threading import Thread
# Create argument parser object
parser = argparse.ArgumentParser()

# Add arguments for value_field and temp_file
parser.add_argument('--value_field', help='name of field containing value', required=True)
parser.add_argument('--temp_file', help='path of the temporary file', required=True)

# Parse the command line arguments
args = parser.parse_args()

# Get the value of value_field and temp_file from the parsed arguments
value_field = args.value_field
temp_file_path = args.temp_file

# Create a gauge metric with topics
g = Gauge(value_field, 'My gauge description', ['topic'])

# Function to consume messages from Kafka topic and update the metric for each mode
def consume_messages(consumer, topic):
    for message in consumer:
        # Convert the message value to a dictionary
        data = eval(message.value)

        # Extract the topic and value from the dictionary
        value = data[value_field]

        # Set the gauge value for the topic
        g.labels(topic).set(value)

# Read the topic names from the temporary file
with open(temp_file_path, 'r') as f:
    topics = [t.strip() for t in f.readlines()]

# Create a Kafka consumer instance for each topic and start consuming messages
consumers = []
for topic in topics:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],  # Replace with the Kafka broker addresses
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='my-group'
    )
    t = Thread(target=consume_messages, args=(consumer, topic))
    t.start()
    consumers.append(consumer)

# Start the Prometheus HTTP server
start_http_server(8080)  # Replace with the desired port number

# Keep the main thread alive
try:
    while True:
        pass
except KeyboardInterrupt:
    # Gracefully stop the consumers
    for consumer in consumers:
        consumer.close()
