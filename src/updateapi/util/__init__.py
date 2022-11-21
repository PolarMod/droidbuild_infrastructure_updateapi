from typing import List, Dict

def todo(fn):
    def wrapped(*args, **kwargs):
        raise NotImplementedError(f"Method {fn.__name__} is not yet implemented")
    return wrapped

def check_keys_in_dict(keys: List, dict_: Dict) -> bool:
    for key in dict_:
        if key not in dict_[key]:
            return False
    return True
