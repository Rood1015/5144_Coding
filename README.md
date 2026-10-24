# Key-Value Store Server

## Description
A simple key-value store server built with Python and Flask. It supports adding, retrieving, updating, and deleting key-value pairs through HTTP requests.

## Features
- POST and PUT: Add or update values.
- GET: Retrieve values.
- DELETE: Remove values.
- Thread safety using a lock.
- Timestamped operation logs.
- Error handling for invalid requests and missing keys.

## Requirements
- Python 3
- Flask

## Installation
Make sure Python 3 is installed.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install Flask:

```bash
pip install flask
```

## Run the Server
```bash
python server.py
```

The server runs at `http://127.0.0.1:8080`.

## Demo examples
Use these commands in powershell

Post:
```bash
python -c "import requests; r=requests.post('http://127.0.0.1:8080/name', json={'value':'Ian'}); print(r.status_code, r.json())"
```
Get:
```bash
python -c "import requests; r=requests.get('http://127.0.0.1:8080/name'); print(r.status_code, r.json())"
```
Error handling:
```bash
python -c "import requests; r=requests.get('http://127.0.0.1:8080/missing'); print(r.status_code, r.json())"
```
Delete:
```bash
python -c "import requests; r=requests.delete('http://127.0.0.1:8080/name'); print(r.status_code, r.json())"
```
Using benchmarks:
```bash
python kv_bench.py
```

## Storage and Logs
Data is stored in memory and is lost when the server stops. 
Logs are saved to `logs/operations.log`.

## Limitations
Persistent storage is not currently implemented.