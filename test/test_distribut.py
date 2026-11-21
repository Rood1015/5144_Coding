import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../router"))
)

from consistent_hash import ConsistentHash

KV_STORES = [
    "http://kv1:8080",
    "http://kv2:8080",
    "http://kv3:8080"
]

hash_ring = ConsistentHash(KV_STORES)

distribution = {server: 0 for server in KV_STORES}

# Assign 10,000 different keys to the hash ring
for i in range(10000):
    key = f"key_{i}"
    server = hash_ring.get_node(key)
    distribution[server] += 1

print("Key Distribution:")

for server, count in distribution.items():
    percentage = count / 10000 * 100
    print(f"{server}: {count} keys ({percentage:.2f}%)")
