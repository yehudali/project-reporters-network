from CleanConfig import CleanConfig
from KafkaConsumer import KafkaConsumer
from KafkaPublisher import KafkaPublisher
from TextCleaner import TextCleaner

from CleanOrchestrator import CleanOrchestrator

import logging

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

conf = CleanConfig(logger)

consumer =  KafkaConsumer(bootstrap_servers=conf.bootstrem_server,
    topic_name="raw",
    group_id="clean_text",
    logger=logger
    )

cleaner = TextCleaner(logger)

   
publisher = KafkaPublisher(bootstrap_servers=conf.bootstrem_server,topic_name="clean_text",logger=logger)




cleanOrchestrator = CleanOrchestrator(consumer,cleaner,publisher,logger)

if __name__ == "__main__":
    cleanOrchestrator.run()