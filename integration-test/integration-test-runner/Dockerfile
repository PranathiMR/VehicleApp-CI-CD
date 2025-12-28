FROM python:3.10-slim

WORKDIR /app

# Install the kuksa-client library
RUN pip install kuksa-client

COPY . .

CMD ["python", "test.py"]