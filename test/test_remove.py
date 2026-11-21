
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../router")
    )
)

from consistent_hash import ConsistentHash

KV1 = "http://kv1:8080"
KV2 = "http://kv2:8080"
KV3 = "http://kv3:8080"

NUM_KEYS = 10000

keys = [f"key_{i}" for i in range(NUM_KEYS)]

# Initial ring: three servers
ring_before = ConsistentHash(
    [KV1, KV2, KV3],
    replicas=500
)

# New ring: remove kv2
ring_after = ConsistentHash(
    [KV1, KV3],
    replicas=500
)

# Count keys that changed ownership
moved = 0
remaining = 0

for key in keys:
    old_node = ring_before.get_node(key)
    new_node = ring_after.get_node(key)

    if old_node != new_node:
        moved += 1

    # Verify that no key is assigned to the removed server
    if new_node in [KV1, KV3]:
        remaining += 1

print("Node Removal Test")
print("-----------------")
print(f"Initial servers: 3")
print(f"Remaining servers: 2")
print(f"Removed server: {KV2}")
print(f"Total keys: {NUM_KEYS}")
print(f"Keys moved: {moved} ({moved / NUM_KEYS * 100:.2f}%)")
print(f"Keys remaining on active servers: {remaining}")

if remaining == NUM_KEYS:
    print("PASS: All keys are assigned to active servers.")
else:
    print("FAIL: Some keys have invalid assignments.")
