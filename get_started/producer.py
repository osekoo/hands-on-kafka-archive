import time
import json

from kafka import KafkaProducer

from config import BOOTSTRAP_SERVER, TOPIC_NAME


def data_serializer(data):
    """
    Converts the given data into json format
    :param data: given data to convert into json
    :return: json data
    """
    return json.dumps(data).encode('utf-8')


def send(producer, size):
    for i in range(size):  # loop through the range of size
        message = {'message': i}  # message to send to Kafka in json format
        print(f'Sending {i} ...')
        producer.send(TOPIC_NAME, value=message)  # send message
        time.sleep(1)  # sleep for 1 second

    producer.flush()


def send_with_key(producer, size, key_mod):
    for i in range(size):  # loop through the range of size
        message = {'message': i}  # message to send to Kafka in json format
        print(f'Sending {i} ...')
        key = i % key_mod  # key to send to Kafka used for partitioning
        producer.send(TOPIC_NAME, key=str.encode(f'{key}'), value=message)  # send message with key
        time.sleep(1)  # sleep for 1 second

    producer.flush()


print('connecting the producer to Kafka bootstrap server...')
producer_handler = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER,
                                 value_serializer=data_serializer)  # create a producer handler

if __name__ == "__main__":
    send(producer_handler, 100)  # send 100 messages to Kafka
    # send_with_key(producer_handler, 100, 3)
