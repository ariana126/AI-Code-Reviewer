FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN  pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/
EXPOSE 8080
CMD ["python", "src/infrastructure/http/server.py"]