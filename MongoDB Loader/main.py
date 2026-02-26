from fastapi import FastAPI, UploadFile, File, Form
import uvicorn


from services.GridFSConfig import GridFSConfig
from services.GridFSOrchestrator import MongoLoaderOrchestrator
from services.GridFSStorage import GridFSStorage

import logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

config = GridFSConfig()
gridfs_storage = GridFSStorage(config.mongo_url, logging.getLogger(GridFSStorage.__module__))


mongo_loader_orchestrator = MongoLoaderOrchestrator(gridfs_storage, logger)





app = FastAPI()

@app.post("/upload")
def upload_file(files: UploadFile = File(...), image_id: str = Form(...)):
    request = {
        "file": files.file,
        "image_id": image_id
    }

    mongo_loader_orchestrator.run(request)

    return {"status": "success"}



uvicorn.run(app)
