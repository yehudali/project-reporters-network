from config import *


if __name__ == "__main__":
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
        publisher=kafka
    )
    
    # run:
    orchestrator.run_all_directory()