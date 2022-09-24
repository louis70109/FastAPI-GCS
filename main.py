import os
import tempfile
import logging
from utils.auth import get_current_username
if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv
    logging.info('Dev env file loading.')
    load_dotenv()

import uvicorn
from fastapi import FastAPI, Request, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List

from routers import users, items
from utils.gcp import upload_data_to_gcs

app = FastAPI()

google_temp = tempfile.NamedTemporaryFile(suffix='.json')
try:
    GOOGLE_KEY = os.environ.get('GOOGLE_KEY', '{}')
    google_temp.write(GOOGLE_KEY.encode())
    google_temp.seek(0)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_temp.name
except Exception as e:
    logging.info(f'GCP JSON key format error. {e}')
    google_temp.close()
    raise
    

templates = Jinja2Templates(directory="templates")

app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
async def health():
    return {"message": "Hello World!"}


@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request, username: str = Depends(get_current_username)):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
def upload(files: List[UploadFile] = File(...)):
    for file in files:
        try:
            contents = file.file.read()

            url = upload_data_to_gcs(os.getenv('GOOGLE_BUCKET'), contents, file.filename,
                    meta=file.content_type)
            logging.info(f'GCS upload file link: {url}')
        except Exception as e:
            logging.debug(e)
            logging.warn(f'File upload to GCS fail. Please check GCP json key and bucket.')
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": "Successfully uploaded"}  


if __name__ == "__main__":
    port = os.getenv('PORT', default=5000)
    debug = True if os.getenv('API_ENV', default='develop') == 'develop' else False
    logging.info('FastAPI server ON!')
    logging.info(f'Mode is {debug}.')
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)
