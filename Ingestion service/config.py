import os
from dotenv import load_dotenv
load_dotenv()
import uuid
from PIL import Image 
import easyocr
import requests
import json
from confluent_kafka import Producer
import logging

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

class OCREngine:
    def __init__(self) -> None:
        self.reader = easyocr.Reader(['en'])

    def extract_text(self, Image_path)->list|None:
        try:
            result = self.reader.readtext(Image_path,detail=0) 
            return result
        
        except Exception as e:
            print(e)

class MetadataExtractor:# ID ומטאדאטה
    def __init__(self) -> None:
        pass
    def extract_metadata(self, Image_path:str):   # מחזיר אובייקט מטא־דאטה )גודל קובץ, ממדים, פורמט וכו‘( 
        try:    

            imag_size = os.path.getsize(Image_path)

            with Image.open(Image_path) as img:
                width, height = img.size
                img_format = img.format
               
            return {"imag_size": imag_size,
                "img_format": img_format,
                'img_width':width,
            "img_height": height,
            }
        
        except Exception as e:
            print(e)
    
    def generate_image_id(self) -> str: # יוצר ID חדש
        return str(uuid.uuid4())

class MongoLoaderClient:
    def __init__(self, url):
        self.url = url
    
    def upload_image(self, image_path, image_id):
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.url}/upload?image_id={image_id}", files=files)
                return response.status_code == 200
        except Exception as e:
            print(f"Mongo Upload Error: {e}")
            return False
        
class KafkaPublisher:
    def __init__(self, servers, topic, logger=None):
        conf = {
            'bootstrap.servers': servers,
            'client.id': 'ingestion-service'
        }
        self.producer = Producer(conf)
        self.topic = topic

        self.logger = logger or logging.getLogger(__name__)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def publish(self, data):
        try:
            self.producer.produce(
                topic = self.topic, 
                value=json.dumps(data).encode('utf-8'),
                callback=self.delivery_report
            )
            self.producer.poll(0)
        except Exception as e:
            self.logger.error(f"Kafka Publish Error: {e}")

    def flush(self):
        self.producer.flush()

class IngestionOrchestrator:
    def __init__(self, config:IngestionConfig,  ocr_engine:OCREngine, metadata_extractor:MetadataExtractor, mongo_client:MongoLoaderClient, publisher:KafkaPublisher, logger=None) -> None:
        self.config = config
        self.ocrengine = ocr_engine
        self.metadataextractor = metadata_extractor
        self.mongo_client = mongo_client
        self.publisher = publisher
        self.logger = logger or logging.getLogger(__name__)

    def process_image(self, image_path):
        image_id = self.metadataextractor.generate_image_id()
        self.logger.info(f"Processing image: {image_path} with ID: {image_id}")
        metadata = self.metadataextractor.extract_metadata(image_path)
        raw_text = self.ocrengine.extract_text(image_path)
        

        data_to_publish = {
            "image_id": image_id,
            "metadata": metadata,
            "raw_text":raw_text
        }
    
        if self.mongo_client:
            self.mongo_client.upload_image(image_path, image_id)

        if self.publisher:
            self.publisher.publish(data_to_publish)

        self.logger.info(f"Successfully processed {image_id}")
        return data_to_publish
    

    def run_all_directory(self):
        image_directory =  self.config.IMAGE_DIRECTORY
        if not image_directory:
            self.logger.error(f"Directory {image_directory} does not exist")
            return

        if not os.path.exists(image_directory):
            print(f"erorr: directory {image_directory} not exist")
            return
        
        # זמני: הגבבלת הריצה ל10 אוביקטים
        list_directory = os.listdir(image_directory) ###
        for imag_file_name in list_directory[:10]: ## 
            path = os.path.join(image_directory, imag_file_name)
            try:
                self.process_image(path)
                
                if self.publisher:
                    self.publisher.flush()
            except Exception as e:
                self.logger.error(f"Failed to process file {path}: {e}")
