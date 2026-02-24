import os
from dotenv import load_dotenv
load_dotenv()

class GridFSConfig:
    def __init__(self) -> None:
        self.mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.validate()

    def get_mongo_url(self):
        return self.mongo_url
    
    def validate(self):
        if not self.mongo_url:
            print("i dont loade/have a mongo_url env!")


# con = GridFSConfig()
# print(con.get_mongo_url())