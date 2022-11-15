import logging
import os
import tempfile
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv
    logger.info('Dev env file loading.')
    load_dotenv()

import uvicorn
from fastapi import FastAPI
from routers import upload

app = FastAPI()

google_temp = tempfile.NamedTemporaryFile(suffix='.json')
try:
    GOOGLE_KEY = os.environ.get('GOOGLE_KEY', '{}')
    logger.debug(GOOGLE_KEY)
    google_temp.write(GOOGLE_KEY.encode())
    google_temp.seek(0)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_temp.name
    logger.debug(google_temp.name)
except Exception as e:
    logger.warning(f'GCP JSON key format error. {e}')
    google_temp.close()
    raise

app.include_router(upload.router)

@app.get("/")
async def health():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    port = os.environ.get('PORT', default=8080)
    debug = True if os.environ.get('API_ENV', default='develop') == 'develop' else False
    logger.info('FastAPI server ON!')
    logger.info(f'Mode is {debug}.')
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=debug)
