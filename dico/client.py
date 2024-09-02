import json
import threading

from kafka import KafkaConsumer, KafkaProducer

from config import BOOTSTRAP_SERVER, TOPIC_DICO_FR, TOPIC_DICO_EN
from kafka_data import KafkaRequest, KafkaResponse


class KafkaClient:

    def __init__(self, dico_topic_name: str, response_topic_name: str):
        self.dico_topic_name = dico_topic_name
        self.response_topic_name = response_topic_name
        self.producer = None
        self.consumer = None
        self.running = True

    def connect(self):
        """
        Connects the producer (sending word request) and the consumer (reading the definition) to Kafka
        """
        self.producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER,
                                      value_serializer=self.data_serializer)

        self.consumer = KafkaConsumer(self.response_topic_name,
                                      bootstrap_servers=BOOTSTRAP_SERVER,
                                      value_deserializer=self.data_deserializer,
                                      auto_offset_reset='earliest',
                                      enable_auto_commit=True,
                                      group_id=self.response_topic_name + '-group')

    def produce(self):
        """
        Reads the words from the shell and sends them to the Kafka topic
        """
        if not self.producer:
            self.connect()
        word = None
        while word != '':
            word = input('Enter the word to search (or press Enter to finish) > ')  # read word from the shell
            if word == '':
                print('shutting down...')
                break
            data = KafkaRequest(word.strip(), self.response_topic_name)
            self.producer.send(self.dico_topic_name, data)
        self.running = False

    def bulk_search_words(self, words):
        """
        Sends the given words to the Kafka topic
        """
        if not self.producer:
            self.connect()
        for word in words:
            data = KafkaRequest(word, self.response_topic_name)
            self.producer.send(self.dico_topic_name, data)
        self.running = False
        print('Done.')

    def read_definition(self):
        """
        Reads the definition of the words from the Kafka topic
        """
        if not self.consumer:
            self.connect()

        while self.running:
            items = self.consumer.poll(timeout_ms=1000)  # read the definition from the Kafka topic in non-blocking mode
            if not self.running:
                break
            for values in items.values():  # iterate over the values of the items
                for data in values:
                    print('\n================= Definition of `', data.value.word, '`=================')
                    print(data.value.definition)
                    print('================= End of definition =================')
                self.consumer.commit()

        print('Stop reading definition.')
        print('Bye.')

    @staticmethod
    def data_deserializer(data) -> KafkaResponse:
        """
        Converts the given data into json format
        :param data: given data to convert into json
        :return: KafkaRequest data
        """
        jdata = json.loads(data.decode('utf-8'))
        return KafkaResponse(**jdata)

    @staticmethod
    def data_serializer(data: KafkaRequest):
        """
        Converts the given data into json format
        :param data: given data to convert into json
        :return: json data
        """
        return json.dumps(data.__dict__).encode('utf-8')


if __name__ == "__main__":
    your_name = input('Your nickname? ')  # read the user's nickname from the shell (to create a unique topic name)
    dico_name = input('Which dictionary ([fr]/en)? ')  # read the dictionary name from the shell (fr or en)
    topic = TOPIC_DICO_EN if dico_name == 'en' else TOPIC_DICO_FR  # set the topic name based on the dictionary name
    def_producer = KafkaClient(topic, topic + '-' + your_name)  # create a Kafka client

    reading_thread = threading.Thread(target=def_producer.read_definition)  # create a thread to read the definition
    reading_thread.start()  # start the thread

    print(f'dico client \'{topic}\' started.')
    def_producer.produce()  # start the producer

    # read the words from the file and send them to the Kafka topic in bulk
    # with open('words_fr.txt', 'r') as f:
    #     word_list = f.read().splitlines()
    # def_producer.search_words(word_list)  # search the words from the file
