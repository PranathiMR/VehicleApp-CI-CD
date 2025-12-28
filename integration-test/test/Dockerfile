FROM python:3.11-slim

WORKDIR /test

RUN pip install kuksa-client

COPY test.py .

CMD ["python", "test.py"]
