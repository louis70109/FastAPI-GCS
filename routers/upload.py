import os
from typing import List
from fastapi import APIRouter,Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils.gcp import upload_data_to_gcs
from utils.auth import get_current_username
import logging
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def upload_page(request: Request, username: str = Depends(get_current_username)):
    logger.debug("Basic login success.")
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/")
def upload(files: List[UploadFile] = File(...), username: str = Depends(get_current_username)):
    for file in files:
        try:
            contents = file.file.read()
            logger.debug(f'content file is {contents}')
            url = upload_data_to_gcs(os.getenv('GOOGLE_BUCKET'), contents, file.filename,
                    meta=file.content_type)
            logger.debug(f'GCS upload file link: {url}')
        except Exception as e:
            logger.warning(e)
            logger.warn(f'File upload to GCS fail. Please check GCP json key and bucket.')
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": "Successfully uploaded"}  
