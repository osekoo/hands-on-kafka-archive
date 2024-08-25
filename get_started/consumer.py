import time
import json

from kafka import KafkaConsumer

from config import BOOTSTRAP_SERVER, TOPIC_NAME


def data_deserializer(data):
    """
    Converts the given data into json format
    :param data: given data to convert into json
    :return: json data
    """
    return json.loads(data.decode('utf-8'))


def receive(consumer):
    for data in consumer:
        print('Hello:', data.value)
        # time.sleep(1)


print('connecting the consumer to Kafka bootstrap server...')
consumer_handler = KafkaConsumer(TOPIC_NAME,
                                 bootstrap_servers=BOOTSTRAP_SERVER,
                                 value_deserializer=data_deserializer,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 group_id='my-consumer-group')

if __name__ == "__main__":
    print('reading data from Kafka...')
    receive(consumer_handler)
