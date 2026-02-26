from pymongo import MongoClient
import gridfs
from logging import Logger

# אחראי על שמירת הקובץ הבינארי ב־MongoDB באמצעות GridFS

class GridFSStorage:
    def __init__(self, mongo_url, logger:Logger) -> None:
        self.logger  = logger

        self.mongo_url= mongo_url

        self.client = MongoClient(mongo_url)
        self.db = self.client['db_files']
        self.collection = self.db['files']

        self.fs = gridfs.GridFS(self.db)

    def save(self, file_path, id_image):
        try:
            self.logger.info("try to send to mongo")
            with open(file_path, 'rb') as file_data:
                file_id = self.fs.put(file_data,file_id=id_image)
                self.logger.info(f"File uploaded with file_id: {file_id}")
                return True
        except Exception as e:
            self.logger.error(f"erorr saving image-{id_image}\n :{e}")

        
# x =GridFSStorage("mongodb://root:root123@localhost:27017")
# x.save(r"C:\Users\yehuda\Desktop\project-reporters-network\data\tweet_images\tweet_2.png", 1111)
