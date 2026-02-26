from logging import Logger
from requests import Request
# מקבל בקשות POST מה־Ingestion ושומר את הקובץ במסד הנתונים


class MongoLoaderOrchestrator:
    def __init__(self, storage, logger:Logger) -> None:
        self.storage = storage
        self.logger = logger

    def handle_upload(self, request):
        self.logger.info("start   def handle_upload(self):")
        self.storage.save(
            request["file"],
            request["image_id"]
        )
    def run(self, request):
        self.handle_upload(request)
