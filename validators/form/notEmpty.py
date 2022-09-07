def not_empty(value):
    if isinstance(value, str) and len(value) == 0:
        raise ValueError('should not be empty.')
    return value
