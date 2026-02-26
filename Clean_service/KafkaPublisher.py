from confluent_kafka import Producer
import json

class KafkaPublisher:
    def __init__(self, bootstrap_servers, topic_name, logger) -> None:
        self.bootstrap_servers =bootstrap_servers
        self.topic_name = topic_name
        self.logger = logger

        self.config = {
            'bootstrap.servers':self.bootstrap_servers,
            'client.id':'Clean_service',
            'acks': 'all',
            'retries': 3
        }
        self.producer = Producer(self.config)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def publish(self, event:dict):
        self.event = json.dumps(event)
        self.producer.produce(
                        topic=self.topic_name,
                        value=self.event.encode(),
                       callback=self.delivery_report
        )
        
        self.producer.flush()
