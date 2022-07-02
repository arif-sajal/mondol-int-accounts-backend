def not_empty(value):
    if value is '':
        raise ValueError('should not be empty.')
    return value
