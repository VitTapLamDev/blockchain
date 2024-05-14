import hashlib
import json

def crypto_hash(*args):
    """
    Return a sha-256 hash of given data
    """
    stringifield_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringifield_args)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"Cypto_hash('one', 2, [3]): {crypto_hash('one', 2, [3])}")

if __name__ == '__main__':
    main()