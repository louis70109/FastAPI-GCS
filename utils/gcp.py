from google.cloud import storage


def upload_data_to_gcs(bucket_name, data, target_key, meta=None):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(target_key)
        blob.upload_from_string(data, content_type=meta)
        return blob.public_url

    except Exception as e:
        print(e)
        raise