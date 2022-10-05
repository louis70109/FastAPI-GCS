FROM python:3.7

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app
EXPOSE 8080
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app