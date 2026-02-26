from confluent_kafka import Consumer
from logging import Logger
import json

class KafkaConsumer:
    def __init__(self, bootstrap_servers, topic_name, group_id, logger:Logger) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic_name = topic_name
        self.group_id = group_id
        self.logger = logger

        self.config = {
            'bootstrap.servers':self.bootstrap_servers,
            'group.id': 'Clean_service',
            'auto.offset.reset': 'earliest', 
            'enable.auto.commit': True,  
            'auto.commit.interval.ms': 5000


        }

    def start(self):
        self.consumer = Consumer(self.config)
        self.consumer.subscribe([self.topic_name])

        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    self.logger.error(msg.error())
                    continue

                # key = msg.value().decode() if msg.value else None
                value = msg.value().decode()
                return json.loads(value)
 
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()