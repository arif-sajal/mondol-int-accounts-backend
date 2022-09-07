import datetime

from fastapi import APIRouter, Response, status, Depends
from odmantic.bson import ObjectId
from typing import List

# Import Models
from models.role import Role
from models.admin import Admin

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.options import make as make_options
from helpers.role import Role as RoleHelper
from helpers.auth import Auth

# Import Forms
from models.forms.role import RoleForm

# Import Responses
from models.response.role import \
    RolesPaginatedResults, \
    RoleResponse
from models.response.common import ErrorResponse, NotFound

api = APIRouter(
    prefix='/v1/role',
    tags=["Roles"],
    dependencies=[Depends(Auth().wrapper)]
)


@api.post(
    '/get-paginated',
    description='Get roles with or without advanced filters.',
    responses={
        200: {'model': RolesPaginatedResults}
    }
)
async def get_paginated_roles(pagination: PaginationParameters):
    results = await prepare_result(Role, pagination)
    return results


@api.get(
    '/get-as-options',
    description='Get role with filters as options.',
    responses={
        200: {'model': List[Role]}
    }
)
async def get_role_options(query: str = ''):
    results = await make_options(Role, ['name'], query)
    return results


@api.get(
    '/get/{rid}',
    description='Get Single Role.',
    responses={
        200: {'model': Role},
        404: {'model': NotFound}
    }
)
async def get_single_role(rid: ObjectId, response: Response):
    role = await db.find_one(Role, Role.id == rid)
    if role is not None:
        return role

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'role'],
        msg='Role Not Found'
    )


@api.post(
    '/create',
    description='Create new Role.',
    responses={
        200: {'model': RoleResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_role(rof: RoleForm, response: Response):
    modules = RoleHelper().get_prepared_modules_from_model(rof.modules)
    role = Role(
        name=rof.name,
        description=rof.description,
        modules=modules
    )

    try:
        await db.save(role)
        return RoleResponse(
            loc=['create', 'role', 'success'],
            msg='Role created successfully.',
            data=role
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'role', 'error'],
            msg='Can\'t create role now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{rid}',
    description='Update role.',
    responses={
        200: {'model': RoleResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def update_role(rid: ObjectId, rof: RoleForm, response: Response):
    role = await db.find_one(Role, Role.id == rid)

    if role is not None:
        modules = RoleHelper().get_prepared_modules_from_model(rof.modules)
        role.name = rof.name
        role.description = rof.description
        role.modules = modules
        role.updated_at = datetime.datetime.utcnow()

        try:
            await db.save(role)
            return RoleResponse(
                loc=['update', 'role', 'success'],
                msg='Role updated successfully.',
                data=role
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'role', 'error'],
                msg='Can\'t update role now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['role', 'not', 'found'],
        msg='Role not found with the provided ID.'
    )


@api.get(
    '/change-status/{rid}',
    description='Change role activation status.',
    responses={
        200: {'model': RoleResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def change_role_activation_status(rid: ObjectId, response: Response):
    role = await db.find_one(Role, Role.id == rid)

    if role is not None:
        role.active = not role.active

        try:
            await db.save(role)
            return RoleResponse(
                loc=['update', 'role', 'success'],
                msg='Role status changed successfully.',
                data=role
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'role', 'error'],
                msg='Can\'t change role status now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['role', 'not', 'found'],
        msg='Role not found with the provided ID.'
    )


@api.delete(
    '/delete/{rid}',
    description='Delete Role.',
    responses={
        200: {'model': RoleResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def delete_role(rid: ObjectId, response: Response):
    role = await db.find_one(Role, Role.id == rid)
    if role is not None:
        admins = len(await db.find(Admin, Admin.role == role.id))
        if admins > 0:
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'role', 'error'],
                msg=f'Can\'t delete this role, {admins} Admins exists on this role.'
            )
        else:
            try:
                await db.delete(role)
                return RoleResponse(
                    loc=['delete', 'role', 'success'],
                    msg='Role deleted successfully.',
                    data=role
                )
            except():
                response.status_code = status.HTTP_403_FORBIDDEN
                return ErrorResponse(
                    loc=['delete', 'role', 'error'],
                    msg='Can\'t delete role now, Please try again or contact administrator'
                )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['role', 'not', 'found'],
        msg='Role not found with the provided ID.'
    )
