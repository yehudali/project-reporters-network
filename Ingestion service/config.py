import os
from dotenv import load_dotenv
load_dotenv()
import uuid
from PIL import Image 
import easyocr


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
    
    

class MetadataExtractor:
    def __init__(self) -> None:
        pass
    def extract_metadata(self, Image_path:str):   # מחזיר אובייקט מטא־דאטה )גודל קובץ, ממדים, פורמט וכו‘( 
        try:    

            imag_size = os.path.getsize(Image_path)

            with Image.open(Image_path) as img:
                width, height = img.size
                img_format = img.format
               
            return {"img_size": imag_size,
                "img_format": img_format,
                'img_width':width,
            "img_height": height,
            }
        
        except Exception as e:
            print(e)
    
    def generate_image_id(self) -> str: # יוצר ID חדש
        return str(uuid.uuid4())

