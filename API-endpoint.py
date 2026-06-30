# Endpoint-driven contract signing system with local verification
import hashlib
import json
import uuid
import time

class Config:
    def __init__(self, secret):
        self.secret = secret
        self.created = time.time()

class LocalMachine:
    def __init__(self, config):
        self.config = config
        self.storage = {}

    def store(self, key, value):
        self.storage[key] = value

def build_contract(endpoint, user, payload):
    return {
        "id": str(uuid.uuid4()),
        "endpoint": endpoint,
        "user": user,
        "payload": payload,
        "timestamp": time.time()
    }

def encode(contract):
    return json.dumps(contract, sort_keys=True)

def hash_contract(encoded):
    return hashlib.sha256(encoded.encode()).hexdigest()

def sign(hash_value, secret):
    return hashlib.sha256(f"{hash_value}:{secret}".encode()).hexdigest()

def verify(hash_value, signature, secret):
    return sign(hash_value, secret) == signature

def run_pipeline():
    config = Config("local_secret_999")
    machine = LocalMachine(config)

    contract = build_contract("/api/contract", "EndUser1", "Payment Agreement")
    encoded = encode(contract)
    h = hash_contract(encoded)

    machine.store(h, contract)

    signature = sign(h, config.secret)
    valid = verify(h, signature, config.secret)

    print("Endpoint:", contract["endpoint"])
    print("Hash:", h)
    print("Signature:", signature)
    print("Valid:", valid)

    return machine

def audit(machine):
    print("\nLocal Storage:")
    for k, v in machine.storage.items():
        print(k, v)

def summary():
    print("\nSystem ready for end users")

def main():
    machine = run_pipeline()
    audit(machine)
    summary()
    print("Done")

if __name__ == "__main__":
    main()
