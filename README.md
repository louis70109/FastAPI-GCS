# FastAPI GCS Example

- GET  '/': Health check.
- Basic Auth. (default: admin/admin)
  - GET  '/upload/': Upload file page.
  - POST '/upload/': Upload multi-file API.

## Prerequisite

- Python 3.7+

## Development

```shell
pip install -r requirements.txt 
pytest tests
python main.py
```

or 

```shell
docker-compose up
```

```shell
curl http://localhost:5000/
```