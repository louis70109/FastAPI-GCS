from google.cloud import storage
import logging
logger = logging.getLogger(__name__)

def upload_data_to_gcs(bucket_name, data, target_key, meta=None):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(target_key)
        blob.upload_from_string(data, content_type=meta)
        logger.debug(f"Upload success, URL is {blob.public_url}")

        return blob.public_url

    except Exception as e:
        logger.error("Failure to upload to GCS.")
        logger.error(e)
        raise