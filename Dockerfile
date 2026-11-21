FROM python:3.12-alpine AS kv-store

WORKDIR /kv-store

RUN pip install flask requests

COPY kv-store/server.py .

EXPOSE 8080

CMD ["python", "server.py"]



FROM python:3.12-alpine AS router

WORKDIR /router

RUN pip install flask requests

COPY router/router.py .

COPY router/consistent_hash.py .

EXPOSE 5555

CMD ["python", "router.py"]