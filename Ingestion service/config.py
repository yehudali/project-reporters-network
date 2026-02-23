import os
from dotenv import load_dotenv
load_dotenv()

class IngestionConfig:
    def __init__(self) -> None:
        load_dotenv()
        self.IMAGE_DIRECTORY = os.getenv('IMAGE_DIRECTORY')
        self.KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
        self.KAFKA_TOPIC_RAW = os.getenv("KAFKA_TOPIC_RAW")
        self.MONGO_LOADER_URL = os.getenv("MONGO_LOADER_URL")
        self.validate()

    def validate(self):
        if not self.IMAGE_DIRECTORY:
            raise ValueError('i not have IMAGE_DIRECTORY env')
        if not self.KAFKA_BOOTSTRAP_SERVERS:
            raise ValueError('i not have KAFKA_BOOTSTRAP_SERVERS env')
        if not self.MONGO_LOADER_URL:
            raise ValueError("i not have MONGO_LOADER_URL env")


