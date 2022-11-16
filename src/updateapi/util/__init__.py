def todo(fn):
    def wrapped(*args, **kwargs):
        raise NotImplementedError(f"Method {fn.__name__} is not yet implemented")
    return wrapped
