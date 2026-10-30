FROM python:3.12-alpine

WORKDIR /kv-store

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY kv-store/server.py .

EXPOSE 8080

CMD ["python", "server.py"]