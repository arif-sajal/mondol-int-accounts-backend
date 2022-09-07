def not_same_currencies(v):
    if not isinstance(v, list):
        raise ValueError('invalid values given.')
    else:
        vs = list(map(lambda c: c.currency, v))
        if len(vs) is not len(set(vs)):
            raise ValueError('can be used once under one account.')
        return v
