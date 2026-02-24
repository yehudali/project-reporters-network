from config import *
from logger import AppLogger

if __name__ == "__main__":

    app_logger = AppLogger.get_logger("IngestionService")

    cfg = IngestionConfig()
    
    ocr = OCREngine()

    meta = MetadataExtractor()

    mongo = MongoLoaderClient(cfg.MONGO_LOADER_URL)

    kafka = KafkaPublisher(cfg.KAFKA_BOOTSTRAP_SERVERS, cfg.KAFKA_TOPIC_RAW)
    

    orchestrator = IngestionOrchestrator(
        config=cfg, 
        ocr_engine=ocr, 
        metadata_extractor=meta, 
        mongo_client=mongo, 
        publisher=kafka,
        logger=app_logger
    )
    
    # run:
    orchestrator.run_all_directory()