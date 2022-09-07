# Import Helpers
from helpers.database import db

# Import Utils
from bson import objectid


async def make(model, params, query):
    q = _make_queries(params, query)
    results = await db.find(model, q)
    return results


def _make_queries(params, query):
    mqs = query.split(',')
    q = list()
    for mq in mqs:
        if objectid.ObjectId.is_valid(mq):
            q.append({'_id': {'$eq': objectid.ObjectId(mq)}})
        else:
            for param in params:
                q.append({param: {'$regex': f'.*{mq}', '$options': 'i'}})
    return {'$or': q}
