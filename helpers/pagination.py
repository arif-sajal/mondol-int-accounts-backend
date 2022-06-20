from pydantic import BaseModel, Field
from odmantic.bson import BaseBSONModel
from typing import List, TypedDict, Optional, Any
from enum import Enum

# Import Helpers
from helpers.database import db

# Import Utils
from odmantic import ObjectId


class FilterType(str, Enum):
    str = 'str'
    int = 'int'
    bool = 'bool'
    id = 'id'


class DataFilters(TypedDict):
    field: str
    operator: str
    type: Optional[FilterType]
    value: Any


class PaginationParameters(BaseModel):
    page: int = Field(default=0)
    limit: int = Field(default=10)
    filters: Optional[List[DataFilters]]


class PaginationResult(BaseBSONModel):
    """
    Pagination Result Class
    with multiple must need values for paginated result
    """
    page: int = Field(default=0)
    limit: int = Field(default=10)
    filtered_total: int = Field(default=0)
    total: int = Field(default=0)
    data: Optional[List]


async def prepare_result(model, param: PaginationParameters):
    skip = param.page * param.limit
    prepared_filters = param.filters is not None and _prepare_filters(param.filters)
    total = await db.count(model=model)

    if param.filters is not None:
        filtered_total = await db.count(model, prepared_filters)
        results = await db.find(model, prepared_filters, skip=skip, limit=param.limit)
    else:
        filtered_total = total
        results = await db.find(model, skip=skip, limit=param.limit)

    return PaginationResult(
        page=param.page,
        limit=param.limit,
        filtered_total=filtered_total,
        total=total,
        data=results
    )


def _prepare_filters(filters):
    prepared_filters = dict()
    for fil in filters:
        value, filter_value = _prepare_query(fil)
        prepared_filters.update({f'{fil["field"]}': filter_value})
    return prepared_filters


def _prepare_value(sfilter):
    if 'type' in sfilter:
        filter_type = sfilter["type"]

        if filter_type == FilterType.str:
            value = str(sfilter["value"])
        elif filter_type == FilterType.int:
            value = int(sfilter["value"])
        elif filter_type == FilterType.bool:
            value = sfilter["value"] in ['true', 'positive', '1', 1]
        elif filter_type == FilterType.id:
            value = ObjectId(sfilter["value"])
        else:
            value = sfilter["value"]
    else:
        value = sfilter["value"]

    return value


def _prepare_query(sfilter):
    value = _prepare_value(sfilter)

    if 'operator' in sfilter:
        operator = sfilter["operator"]

        if operator == 'icontains':
            filter_value = {'$regex': f'.*{value}*.', '$options': 'i'}
        elif operator == 'contains':
            filter_value = {'$regex': f'.*{value}*.'}
        elif operator == 'istartswith':
            filter_value = {'$regex': f'^{value}', '$options': 'i'}
        elif operator == 'startswith':
            filter_value = {'$regex': f'^{value}'}
        elif operator == 'iendswith':
            filter_value = {'$regex': f'{value}$', '$options': 'i'}
        elif operator == 'endswith':
            filter_value = {'$regex': f'{value}$'}
        elif operator == 'iexaact':
            filter_value = {'$regex': f'^{value}$', '$options': 'i'}
        elif operator == 'exact':
            filter_value = {'$regex': f'^{value}$'}
        else:
            filter_value = {f'${sfilter["operator"]}': value}
    else:
        filter_value = {f'$eq': value}

    return value, filter_value
