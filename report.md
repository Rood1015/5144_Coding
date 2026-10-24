# Key-Value Store Server Report

## 1. Design Decisions and justification

I used Python and Flask to build the key-value store server. I chose Flask because it makes handling HTTP requests and JSON data easier. The server runs on port 8080 and uses a Python dictionary to store keys and values. It supports GET to retrieve values, POST/PUT to add or update values, and DELETE to remove keys. I also made it to support POST because the provided benchmark uses POST requests for writing data. I used a thread lock to protect shared storage when multiple requests access it concurrently.

## 2. Challenges and Solutions

One challenge was handling concurrent requests without causing problems with the stored data. I addressed this by using a thread lock around dictionary operations. Another challenge was matching the provided benchmark's request and response formats. I tested the server using the expected JSON format and checked that it returned the correct values and appropriate HTTP status codes.

## 3. Assumptions
I assumed that in-memory storage was sufficient for the basic version of the project. The server stores keys and values while it is running. However, the data is lost when the server stops. When a key already exists, a write operation replaces its previous value. If a requested key does not exist, the server returns a 404 error.

## 4. Future Improvements

Future improvements could include saving data to a file or database so it could save datas after server stops or restarts. I could also perform more extensive concurrency and performance tests, improve input validation, and test the server with larger workloads.