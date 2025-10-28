FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN  pip install -r requirements.txt

COPY src/ /app/src/

ENV PYTHONPATH=/app/src
EXPOSE 8080

#CMD ["python", "src/infrastructure/http/server.py"]
CMD ["python", "-m", "vericon.infrastructure.http.server"]