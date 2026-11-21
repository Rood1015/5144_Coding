# Distributed Key-Value Store Using Consistent Hashing

## 1. Introduction

For this project, we worked on extending our previous key-value store so that it could handle requests using multiple servers instead of only one server. The main idea was to distribute keys across different key-value stores using consistent hashing.

When a system uses only one server, that server has to handle all incoming requests. This can become a problem when the number of requests increases. By using multiple servers, we wanted to distribute the workload and see whether the system could achieve better performance.

We implemented a router that receives requests from clients and uses consistent hashing to decide which key-value store should handle each key. We then tested the system with one, two, and three key-value stores to compare key distribution, membership changes, throughput, and latency.

The main goals of this project were:

- Implement consistent hashing to distribute keys across multiple servers.
- Support different numbers of key-value store instances.
- Check how key assignments change when servers are added.
- Compare throughput and latency with one, two, and three servers.
- Understand the performance improvements and limitations of the system.

## 2. System Architecture

Our system has two main components: the router and the key-value stores.

### 2.1 Key-Value Store

Each key-value store is implemented using Python and Flask. It stores data as key-value pairs in a Python dictionary.

The server supports four main operations:

- **POST:** Store a new key-value pair.
- **PUT:** Add or update a key-value pair.
- **GET:** Retrieve the value of a key.
- **DELETE:** Remove a key-value pair.

We also used a threading lock when accessing the dictionary. This helps prevent problems when multiple requests try to access or modify the stored data at the same time.

### 2.2 Router

The router is responsible for receiving requests from clients and sending them to the correct key-value store.

Instead of making clients communicate directly with each server, clients only need to send requests to the router. The router checks the requested key, uses consistent hashing to select a server, and forwards the request.

For example, if a client sends a GET request for a key, the router finds which server is responsible for that key and sends the request to that server. The response is then returned to the client.

The router supports POST, PUT, GET, and DELETE operations. It also handles situations where a selected server cannot be reached.

### 2.3 Consistent Hashing

We implemented consistent hashing in `router/consistent_hash.py`.

The implementation uses SHA-256 to generate hash values for both keys and servers. Each server is assigned multiple virtual nodes on the hash ring. We used 100 virtual nodes per server by default.

When the system receives a key, it first calculates the key's hash value. It then searches the sorted hash ring to find the next server position that is greater than or equal to the key's hash. If the search reaches the end of the ring, it wraps around to the beginning.

This allows the system to determine which server should handle a specific key.

We also implemented methods to add and remove servers from the ring. This is important because the number of servers can change over time. Virtual nodes also help make the key distribution more balanced.

### 2.4 Docker Configuration

We used Docker Compose to run the router and multiple key-value store instances.

Our configuration contains three key-value store services (`kv1`, `kv2`, and `kv3`) and one router service.

The router gets the server addresses through the `KV_STORES` environment variable. This makes it possible to configure the router with a different number of servers without changing the main router implementation.

When the server configuration changes, the router needs to be restarted so that it can build the hash ring using the updated list of servers.

## 3. Implementation

### 3.1 Key-Value Store

The key-value store implementation is located in `kv-store/server.py`.

We used a Python dictionary to store the data. The server handles incoming HTTP requests and performs the requested operation on the dictionary.

We added a threading lock around storage operations to make sure that multiple requests do not modify the shared dictionary at the same time without protection.

The server also checks incoming JSON data. For example, if a request does not contain the required `value` field, it returns an HTTP 400 response. If a client requests a key that does not exist, the server returns HTTP 404.

### 3.2 Router

The router implementation is located in `router/router.py`.

When the router starts, it reads the available key-value store addresses from the `KV_STORES` environment variable and creates the consistent hashing ring.

When a request comes in, the router uses the key to find the correct server. After selecting the server, it forwards the request and returns the response to the client.

This design makes it easier for clients to use the distributed system because they do not need to know which server stores each key.

### 3.3 Consistent Hashing

The main hashing logic is located in `router/consistent_hash.py`.

We used SHA-256 for hashing and 100 virtual nodes for each server. The hash positions are stored in a dictionary, while a sorted list is used to search for the correct server.

The implementation uses Python's `bisect` module to find the correct position on the ring. This avoids checking every server position one by one.

The class also supports adding and removing nodes. We used these functions to test how the key assignments change when the number of servers increases.

## 4. Testing Methodology

We performed several tests to check whether the system worked correctly and how its performance changed with different numbers of servers.

### 4.1 Basic Operations

First, we tested the basic operations of the key-value store:

- POST
- PUT
- GET
- DELETE

We checked whether values could be stored, retrieved, updated, and deleted correctly. We also checked how the server handled invalid requests and requests for keys that did not exist.

### 4.2 Key Distribution Test

We used `test/test_distribut.py` to check how evenly keys were distributed across three servers.

The test generated 10,000 keys and used consistent hashing to determine which server each key belonged to. We then counted how many keys were assigned to each server.

### 4.3 Membership Change Test

We used `test/test_member.py` to check what happens when the number of servers changes.

The test generated 10,000 keys and compared their assignments under different configurations:

1. One server.
2. Two servers.
3. Three servers.

We counted how many keys were assigned to a different server after adding another server.

This helped us understand how the hash ring changes when new servers are added.

### 4.4 Performance Benchmark

We used `kv_bench.py` to measure the performance of the system.

The benchmark used three worker threads, with 100 operations per thread. This resulted in 300 keys and 300 write operations followed by 300 read operations.

During the write phase, the benchmark stored values in the system. During the read phase, it retrieved those values and checked whether they matched the expected values.

We measured the following:

- Successful operations
- Mismatched values
- Errors
- Total execution time
- Throughput (operations per second)
- Average latency
- 99th-percentile latency (p99)

We ran the benchmark with one, two, and three key-value store instances to compare the results.

## 5. Testing Results

### 5.1 Key Distribution Results

We generated 10,000 keys and distributed them across three key-value store instances.

| Key-Value Store | Number of Keys | Percentage |
|---|---:|---:|
| kv1 | 3,347 | 33.47% |
| kv2 | 3,832 | 38.32% |
| kv3 | 2,821 | 28.21% |
| **Total** | **10,000** | **100%** |

The results show that all three servers received a portion of the keys.

The distribution was not exactly equal. For example, kv2 received 38.32% of the keys, while kv3 received 28.21%. However, the keys were still spread across all three servers instead of being assigned to only one server.

This shows that our consistent hashing implementation can distribute keys across multiple servers, although the distribution is not perfectly balanced.

### 5.2 Membership Change Results

Next, we tested how many keys changed their assigned server when we added more servers.

| Membership Change | Keys Moved | Percentage |
|---|---:|---:|
| 1 to 2 servers | 5,128 | 51.28% |
| 2 to 3 servers | 3,291 | 32.91% |

When we increased the number of servers from one to two, 5,128 out of 10,000 keys changed their assignments.

When we increased the number from two to three, 3,291 keys changed their assignments.

These results show that adding a server changes the key assignments on the hash ring. The test measures which server is selected for each key before and after the change. It does not mean that the actual stored values were automatically transferred between servers.

### 5.3 Performance Results

We compared the performance of the system using one, two, and three key-value store instances.

| Stores | Operation | Throughput (ops/s) | Average Latency (ms) | p99 Latency (ms) |
|---:|---|---:|---:|---:|
| 1 | SET | 345.2 | 8.65 | 20.14 |
| 1 | GET | 338.9 | 8.83 | 14.75 |
| 2 | SET | 378.3 | 7.91 | 12.03 |
| 2 | GET | 420.9 | 7.09 | 9.90 |
| 3 | SET | 391.7 | 7.62 | 11.83 |
| 3 | GET | 407.1 | 7.36 | 9.84 |

The total benchmark results are shown below.

| Stores | Successful Operations | Total Time (s) | Total Throughput (ops/s) |
|---:|---:|---:|---:|
| 1 | 600 | 1.75 | 342.0 |
| 2 | 600 | 1.51 | 398.4 |
| 3 | 600 | 1.50 | 399.3 |

All configurations completed 600 successful operations. There were no mismatched values or errors in the benchmark results.

### 5.4 Performance Discussion

Based on the results, using two servers improved the total throughput compared to using only one server.

With one server, the total throughput was 342.0 operations per second. With two servers, it increased to 398.4 operations per second, which is about a 16.5% improvement.

When we increased the number of servers to three, the throughput increased slightly to 399.3 operations per second. This is about a 16.8% improvement compared to using one server.

We also saw that average latency generally decreased when we used more servers. For example, the average SET latency decreased from 8.65 ms with one server to 7.62 ms with three servers. The average GET latency decreased from 8.83 ms to 7.36 ms.

However, adding a third server did not provide a large performance improvement. In fact, GET throughput was slightly lower with three servers than with two servers.

This means that adding more servers does not always result in a large increase in performance. The router and communication between services can also affect the total performance. Based on our results, adding a second server provided the biggest improvement in this benchmark.

## 6. Challenges and Solutions

### 6.1 Distributing Keys

One of the main challenges was deciding which server should store or handle each key.

We needed an approach that could support multiple servers and allow the number of servers to change. We used consistent hashing to solve this problem.

By using a hash ring and virtual nodes, the system can assign keys to different servers without depending on a simple modulo calculation.

### 6.2 Handling Multiple Requests

Another challenge was handling multiple requests that access the same storage dictionary.

Since the key-value store uses an in-memory Python dictionary, concurrent requests could access or modify the data at the same time. We used a threading lock around storage operations to help prevent concurrency problems.

### 6.3 Connecting the Router and Key-Value Stores

We also needed to make sure that the router could communicate with the correct key-value store.

We used the `KV_STORES` environment variable to provide the server addresses. The router reads this configuration and uses consistent hashing to select a destination for each request.

This also made testing different numbers of servers easier because we could change the configuration instead of changing the router code.

### 6.4 Measuring Performance

We needed to compare the system using the same workload for each configuration.

To make the comparison more consistent, we used the same benchmark settings for one, two, and three servers. We also checked the retrieved values to make sure that the system was not only responding but returning the correct data.

## 7. Limitations and Future Improvements

Although our system successfully distributes requests across multiple key-value stores, there are still some things that could be improved.

### 7.1 Data Migration

One limitation is that our current membership test only checks how key assignments change when a server is added. It does not automatically transfer existing data to the newly assigned server.

For example, if a key was originally stored on one server but gets assigned to another server after changing the hash ring, the new server may not have that value.

A possible improvement would be implementing data migration or replication. This would help keep existing data accessible when the number of servers changes.

### 7.2 Persistent Storage

Currently, each key-value store uses an in-memory dictionary. This means that stored data will be lost if the server restarts.

In the future, we could use a database or another persistent storage method so that data can remain available after a restart.

### 7.3 Performance Testing

Our benchmark showed that adding a second server improved performance, but adding a third server did not make a large difference.

We could perform more benchmark runs with different numbers of worker threads and more operations. This would help us better understand how the system performs under a larger workload.

### 7.4 Dynamic Server Changes

Currently, the router creates the hash ring when it starts. If we change the server configuration, we need to restart the router.

In the future, we could improve the system so that servers can be added or removed while the router is running.

## 8. Conclusion

In this project, we extended our previous key-value store to support multiple servers using consistent hashing.

We implemented a router that receives client requests and forwards them to the correct key-value store. We also used Docker Compose to run multiple key-value store instances and make it easier to test different configurations.

Our distribution test showed that 10,000 keys could be distributed across three servers. The membership test also showed that key assignments change when additional servers are added.

For performance, the total throughput increased from 342.0 ops/s with one server to 398.4 ops/s with two servers. With three servers, it reached 399.3 ops/s. Average latency also generally decreased as we increased the number of servers.

However, the results did not show a linear performance improvement. The biggest improvement happened when we increased the number of servers from one to two. Adding a third server provided only a small additional improvement.

Overall, this project helped us understand how consistent hashing can be used in a distributed key-value store and how adding more servers can affect its performance. We also learned that distributing keys is only one part of building a distributed system. Handling data migration, persistent storage, and server changes are important areas that could be improved in the future.