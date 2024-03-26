import hashlib


def hash_input(input: str) -> int:
    """ """
    url_hash = hashlib.sha256(input.encode()).hexdigest()
    unique_id = int(url_hash[:8], 16)
    return unique_id
