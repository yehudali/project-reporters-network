from KafkaConsumer import KafkaConsumer
from KafkaPublisher import KafkaPublisher
from TextCleaner import TextCleaner

from logging import Logger

class CleanOrchestrator:
    def __init__(self,  consumer:KafkaConsumer, cleaner:TextCleaner, publisher: KafkaPublisher, logger:Logger) -> None:
        self.consumer = consumer
        self.cleaner = cleaner
        self.publisher = publisher
        self.logger = logger
    # data_to_publish = {
        #     "image_id": image_id,
        #     "metadata": metadata,
        #     "raw_text":raw_text
        # }


    def event_handle(self, event:dict):
        data = event
        data_txt = data["raw_text"]
        clean_txt = self.cleaner.clean_text(data_txt)
        data['raw_text'] = clean_txt
        self.logger.log(1,f"the text {data_txt} clean to {clean_txt}!")
        
        # save it:
        self.publisher.publish(data)


    def run(self):
        while True:
            msg:dict|None = self.consumer.start()
            if msg:
                self.event_handle(msg)
            