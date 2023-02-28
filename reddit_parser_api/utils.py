
def url_issue(data: dict, key_name, min_len=0, max_len=200, key_start=""):
    if not key_name in data:
        return f"No key {key_name}"
    if not max_len >= len(data[key_name]) >= min_len:
        return f"{key_name} length must be from {min_len} to {max_len}"
    if not data[key_name].startswith(key_start):
        return f"{key_name} must starts with {key_start}"
    return False
