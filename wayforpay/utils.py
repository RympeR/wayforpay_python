import hashlib
import hmac


def get_signature(merchant_key: str,
                  signature_separator: str,
                  options: dict,
                  keys: list) -> str:
    hash_str = list()
    for datakey in keys:
        if not options.get(datakey):
            continue
        if isinstance(options[datakey], list):
            for _ in options[datakey]:
                hash_str.append(str(_))
        else:
            hash_str.append(str(options[datakey]))
    hash_str = signature_separator.join(hash_str)
    merchant_key_encoded = bytes(str.encode(merchant_key))
    _hash = hmac.new(merchant_key_encoded, hash_str.encode(
        "utf-8"), hashlib.md5).hexdigest()
    return _hash
