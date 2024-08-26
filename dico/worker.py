import json

from kafka import KafkaConsumer, KafkaProducer

from config import BOOTSTRAP_SERVER, TOPIC_DICO_FR, TOPIC_DICO_EN, LANGUAGE_EN
from crawler import Crawler, CrawlerEN, CrawlerFR
from kafka_data import KafkaRequest, KafkaResponse, KafkaStreamingRequest


class KafkaWorker:

    def __init__(self, topic_name: str, crawler: Crawler):
        self.topic_name = topic_name
        self.crawler = crawler
        self.consumer = None
        self.producer = None

    def connect(self):
        """
        Connects the consumer (reading word request) and the producer (sending back the definition) to Kafka
        :return:
        """
        self.consumer = KafkaConsumer(self.topic_name,
                                      bootstrap_servers=BOOTSTRAP_SERVER,
                                      value_deserializer=self.data_deserializer,
                                      auto_offset_reset='latest',
                                      enable_auto_commit=True,
                                      auto_commit_interval_ms=500,
                                      group_id=self.topic_name + '-group')

        self.producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER,
                                      value_serializer=self.data_serializer)

    def consume(self):
        if not self.consumer:
            self.connect()
        print('reading data from Kafka...')
        for data in self.consumer:
            print('received:', data.value)
            self.__handle_word(data.value)

    def __handle_word(self, data: KafkaRequest):
        """
        Requests the definition of the word and send it back to the requester
        :return:
        """
        print(f'searching {data.word} ...', end=' ')
        word_def = self.crawler.get_definition(data.word)
        print(f'\ndefinition found: {word_def}')
        print(f'done.')
        message = KafkaResponse(data.word, word_def)
        print(f'sending back the definition of {data.word} ...', end=' ')
        self.producer.send(data.response_topic, value=message)
        print(f'done.')

        # Spark streaming add-on
        print(f'sending a request to spark for further operations...', end=' ')
        request = KafkaStreamingRequest(data.word, word_def, data.response_topic)
        self.producer.send('spark-streaming-topic', value=request)
        print(f'done.')

    @staticmethod
    def data_deserializer(data) -> KafkaRequest:
        """
        Converts the given data into json format
        :param data: given data to convert into json
        :return: KafkaRequest data
        """
        jdata = json.loads(data.decode('utf-8'))
        return KafkaRequest(**jdata)

    @staticmethod
    def data_serializer(data: KafkaResponse):
        """
        Converts the given data into json format
        :param data: given data to convert into json
        :return: json data
        """
        return json.dumps(data.__dict__).encode('utf-8')


if __name__ == "__main__":
    dico_name = input('Which dictionary ([fr]/en)? ')
    if dico_name == LANGUAGE_EN:
        worker = KafkaWorker(TOPIC_DICO_EN, CrawlerEN())
    else:
        worker = KafkaWorker(TOPIC_DICO_FR, CrawlerFR())

    print(f'dico worker `{dico_name}` started.')
    worker.consume()
