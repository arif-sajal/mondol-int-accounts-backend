# Import Helpers
from helpers.database import db


async def make(model, params, query):
    q = {'$or': _make_queries(params, query)}
    results = await db.find(model, q)
    return results


def _make_queries(params, query):
    q = list()
    for param in params:
        q.append({param: {'$regex': f'.*{query}', '$options': 'i'}})
    return q
