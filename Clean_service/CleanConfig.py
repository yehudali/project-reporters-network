from logging import Logger
import os

class CleanConfig:
    def __init__(self, logger:Logger=Logger(__module__)) -> None:
        self.cafka_host = os.getenv('KAFKA_HOST')
        self.cafka_port = os.getenv('KAFKA_PORT')
        self.bootstrem_server =  os.getenv('BOOTSTREM_SERVER')

        self.logger = logger

        self.validate()

        
    def validate(self):
        if not self.cafka_host:
            self.logger.error(ValueError("i do not hav- cafka_host ,env"))
            
        if not self.cafka_port:
            self.logger.error(ValueError("i do not hav-cafka_port  ,env"))
            
        if not self.bootstrem_server:
            self.logger.error(ValueError("i do not hav- bootstrem_server ,env"))
    