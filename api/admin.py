from fastapi import APIRouter, Response, status, UploadFile, File
from odmantic.bson import ObjectId
from typing import List

# Import Models
from models.admin import Admin, AdminOut

# Import Helpers
from helpers.database import db
from helpers.pagination import prepare_result, PaginationParameters
from helpers.options import make as make_options
from helpers.auth import Auth

# Import Forms
from models.forms.admin import CreateAdminForm, UpdateAdminForm, ChangeAdminPasswordForm

# Import Validators
from validators.form.roleExists import role_exists

# Import Responses
from models.response.admin import AdminsPaginatedResults, AdminResponse
from models.response.common import ErrorResponse, NotFound

api = APIRouter(
    prefix='/v1/admin',
    tags=["Admins"]
)


@api.post(
    '/get-paginated',
    description='Get admins with or without advanced filters.',
    responses={
        200: {'model': AdminsPaginatedResults}
    }
)
async def get_paginated_admins(pagination: PaginationParameters):
    results = await prepare_result(AdminOut, pagination)
    return results


@api.get(
    '/get-as-options',
    description='Get admins with filters as options.',
    responses={
        200: {'model': List[AdminOut]}
    }
)
async def get_admin_options(query: str = ''):
    results = await make_options(AdminOut, ['name', 'email', 'username', 'phone'], query)
    return results


@api.get(
    '/get/{aid}',
    description='Get Single admin.',
    responses={
        200: {'model': AdminResponse},
        404: {'model': NotFound}
    }
)
async def get_single_admin(aid: ObjectId, response: Response):
    admin = await db.find_one(AdminOut, AdminOut.id == aid)
    if admin is not None:
        return admin

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['get', 'single', 'admin'],
        msg='Country Not Found'
    )


@api.post(
    '/create',
    description='Create new admin.',
    responses={
        200: {'model': AdminResponse},
        403: {'model': ErrorResponse}
    }
)
async def create_admin(caf: CreateAdminForm, response: Response):
    role = await role_exists(caf.role)
    if role is False:
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['body', 'role'],
            msg='Invalid Role Selected.'
        )

    auth = Auth()
    admin = Admin(
        name=caf.name,
        email=caf.email,
        phone=caf.phone,
        username=caf.username,
        password=auth.encode_password(caf.password),
        role=role
    )

    try:
        await db.save(admin)
        return AdminResponse(
            loc=['create', 'admin', 'success'],
            msg='Admin created successfully.',
            data=AdminOut(**admin.dict())
        )
    except():
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['create', 'admin', 'error'],
            msg='Can\'t create admin now, Please try again or contact administrator'
        )


@api.patch(
    '/update/{aid}',
    description='Update country.',
    responses={
        200: {'model': AdminResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def update_admin(aid: ObjectId, uaf: UpdateAdminForm, response: Response):
    if not await role_exists(uaf.role):
        response.status_code = status.HTTP_403_FORBIDDEN
        return ErrorResponse(
            loc=['body', 'role'],
            msg='Invalid Role Selected.'
        )

    admin = await db.find_one(Admin, Admin.id == aid)

    if admin is not None:
        admin.name = uaf.name,
        admin.email = uaf.email,
        admin.phone = uaf.phone,
        admin.username = uaf.username,

        try:
            await db.save(admin)
            return AdminResponse(
                loc=['update', 'admin', 'success'],
                msg='Admin updated successfully.',
                data=AdminOut(**admin.dict())
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['update', 'admin', 'error'],
                msg='Can\'t update admin now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['admin', 'not', 'found'],
        msg='Admin not found with the provided ID.'
    )


@api.delete(
    '/delete/{aid}',
    description='Delete admin.',
    responses={
        200: {'model': AdminResponse},
        403: {'model': ErrorResponse},
        404: {'model': NotFound}
    }
)
async def delete_admin(aid: ObjectId, response: Response):
    admin = await db.find_one(Admin, Admin.id == aid)

    if admin is not None:
        try:
            await db.delete(admin)
            return AdminResponse(
                loc=['delete', 'admin', 'success'],
                msg='Admin deleted successfully.',
                data=AdminOut(**admin.dict())
            )
        except():
            response.status_code = status.HTTP_403_FORBIDDEN
            return ErrorResponse(
                loc=['delete', 'admin', 'error'],
                msg='Can\'t delete admin now, Please try again or contact administrator'
            )

    response.status_code = status.HTTP_404_NOT_FOUND
    return NotFound(
        loc=['admin', 'not', 'found'],
        msg='Admin not found with the provided ID.'
    )