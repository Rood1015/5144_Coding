
import requests
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:5555"
KEY = "shared_key"


def put_value(i):
    return requests.post(
        f"{BASE_URL}/{KEY}",
        json={"value": f"value_{i}"},
        timeout=10
    ).status_code


def delete_value():
    return requests.delete(
        f"{BASE_URL}/{KEY}",
        timeout=10
    ).status_code


# Test 1: Concurrent PUT operations on the same key
print("Test 1: Concurrent PUT operations")

with ThreadPoolExecutor(max_workers=20) as executor:
    statuses = list(executor.map(put_value, range(100)))

print("Successful PUTs:", statuses.count(200))
print("Failed PUTs:", len([s for s in statuses if s != 200]))

# Check the final value
response = requests.get(f"{BASE_URL}/{KEY}", timeout=10)

assert response.status_code == 200
assert response.json()["value"] in [
    f"value_{i}" for i in range(100)
]

print("Final stored value:", response.json()["value"])


# Test 2: Concurrent DELETE operations on the same key
print("\nTest 2: Concurrent DELETE operations")

# Make sure the key exists before deleting
requests.post(
    f"{BASE_URL}/{KEY}",
    json={"value": "delete_me"},
    timeout=10
)

with ThreadPoolExecutor(max_workers=20) as executor:
    statuses = list(executor.map(
        lambda _: delete_value(), range(20)
    ))

print("Successful DELETEs:", statuses.count(200))
print("Not found responses:", statuses.count(404))

# Exactly one deletion should succeed
assert statuses.count(200) == 1
assert statuses.count(404) == 19

print("Concurrency tests passed!")
