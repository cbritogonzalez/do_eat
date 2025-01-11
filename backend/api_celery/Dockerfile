FROM python:3.11.8-slim

WORKDIR /app

RUN mkdir /data

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["celery", "worker", "--loglevel=info", "--pool=solo", "--concurrency=2"]