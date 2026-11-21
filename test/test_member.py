
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../router")
    )
)

from consistent_hash import ConsistentHash

# Use the same server identifiers as router.py
KV1 = "http://kv1:8080"
KV2 = "http://kv2:8080"
KV3 = "http://kv3:8080"

# Test 10,000 keys
keys = [f"key_{i}" for i in range(10000)]

# Create rings with different numbers of servers
ring_1 = ConsistentHash([KV1], replicas=500)
ring_2 = ConsistentHash([KV1, KV2], replicas=500)
ring_3 = ConsistentHash([KV1, KV2, KV3], replicas=500)


def count_moved_keys(old_ring, new_ring):
    moved = 0

    for key in keys:
        if old_ring.get_node(key) != new_ring.get_node(key):
            moved += 1

    return moved


moved_1_to_2 = count_moved_keys(ring_1, ring_2)
moved_2_to_3 = count_moved_keys(ring_2, ring_3)

print("Membership Change Results")
print(f"1 to 2 servers: {moved_1_to_2} keys moved "
      f"({moved_1_to_2 / len(keys) * 100:.2f}%)")

print(f"2 to 3 servers: {moved_2_to_3} keys moved "
      f"({moved_2_to_3 / len(keys) * 100:.2f}%)")
