import hashlib


def generate_cache_key(file_content=None, blob_name=None):
    if file_content is not None:
        if isinstance(file_content, str):
            file_content = file_content.encode("utf-8")  # Convert string to bytes
        return hashlib.sha256(file_content).hexdigest()
    elif blob_name is not None:
        return hashlib.sha256(blob_name.encode('utf-8')).hexdigest()
    else:
        raise ValueError("Either 'file_content' or 'blob_name' must be provided to generate a cache key.")
