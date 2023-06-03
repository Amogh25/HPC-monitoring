from kafka import KafkaConsumer
from prometheus_client import start_http_server, Gauge
from threading import Thread
import psycopg2
import json
import datetime
import pytz
import time
import random
import getpass


# Get the value of value_field and temp_file from the parsed arguments
value_field = input("Enter the Value field:")
temp_file_path = input("Enter the file path:")
table_name=input("Enter the table name:")
# Database connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': input("Enter the database name:"),
    'user': 'postgres',
    'password': getpass.getpass("Enter your password: "),
}

# Read column names from input
column_names = []
print("Enter the column names (enter 'done' when finished):")
while True:
    column = input("Column name: ")
    if column.lower() == "done":
        break
    column_names.append(column.strip())


# Create a gauge metric with topics
g = Gauge(value_field, 'My gauge description', ['topic'])

# Function to consume messages from Kafka topic and update the metric for each mode
def consume_messages(consumer, topic):
    for message in consumer:
        try:
            # Convert the message value to a dictionary
            data = eval(message.value)

            # Extract the value from the message
            value = data[value_field]

            # Set the gauge value for the topic
            g.labels(topic).set(value)

            # Insert JSON object into TimescaleDB
            query = "INSERT INTO {table} (time, {columns}) VALUES (%s, {placeholders})".format(
                table=table_name,
                columns=", ".join(column_names),
                placeholders=", ".join(["%s"] * len(column_names))
            )
            current_time = datetime.datetime.now()
            timestamp_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            values = (timestamp_str,) + tuple(data.get(col) for col in column_names)
            cursor.execute(query, values)
            connection.commit()

        except Exception as e:
            print(e)
            continue
        time.sleep(random.uniform(1, 5))

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

# Connect to TimescaleDB
try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
except Exception as e:
    print("Error connecting to the database:", e)
    exit


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

# Close the database connection
connection.close()
