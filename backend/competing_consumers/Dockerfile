FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY mock_consumer.py .

CMD ["python", "mock_consumer.py"]