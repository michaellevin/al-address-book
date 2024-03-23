import hashlib


def hash_input(input: str) -> int:
    """
    TODO: Implement this function to return a unique integer for a given URL.
    """
    url_hash = hashlib.sha256(input.encode()).hexdigest()
    unique_id = int(url_hash[:5], 16)  # 6-digit hexadecimal number
    return unique_id
