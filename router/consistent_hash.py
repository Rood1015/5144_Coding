import hashlib
import bisect

class ConsistentHash:
    def __init__(self, nodes, replicas=100):
        self.ring = {}
        self.sorted_keys = []
        self.replicas = replicas

        for node in nodes:
            self.add_node(node)

    def _hash(self, key):
        return int(
            hashlib.sha256(key.encode()).hexdigest(), 16
        )

    def add_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node

        self.sorted_keys = sorted(self.ring.keys())

    def get_node(self, key):
        if not self.ring:
            return None

        hash_key = self._hash(key)

        index = bisect.bisect(self.sorted_keys, hash_key)

        if index == len(self.sorted_keys):
            index = 0

        return self.ring[self.sorted_keys[index]]
    
    def remove_node(self, node):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            if key in self.ring:
                del self.ring[key]

        self.sorted_keys = sorted(self.ring.keys())