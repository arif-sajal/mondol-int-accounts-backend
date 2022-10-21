from fastapi import APIRouter, Response, status, Depends
from odmantic import ObjectId

# Import Helpers
from helpers.auth import Auth
from helpers.database import db
from helpers.sms import SMS

# Import Models
from models.admin import Admin
from models.role import Role
from models.client import Client
from models.auth import PhoneLogin, ResetPassword

# Import Forms
from models.forms.auth.login import \
    LoginWithCredentialForm, \
    RequestOtpForPhoneLoginForm, \
    LoginWithPhoneForm, \
    RefreshTokenForm
from models.forms.auth.reset import \
    RequestResetPasswordOtpForm, \
    VerifyResetPasswordOtpForm, \
    ResetPasswordForm

# Import Response
from models.response.auth.login import \
    LoginWithCredentialResponse, \
    LoginErrorResponse, \
    RequestOtpForPhoneLoginResponse, \
    LoginWithPhoneResponse, \
    LoggedInUserResponse
from models.response.auth.reset import \
    RequestResetPasswordOtpResponse, \
    VerifyResetPasswordOtpResponse, \
    ResetPasswordResponse, \
    ResetPasswordErrorResponse

# Import Utils
from datetime import datetime, timedelta
import random

api = APIRouter(
    prefix='/v1/auth',
    tags=["Authentication"],
)


@api.post(
    '/login-with-credential',
    description='Login with username and password.',
    responses={
        200: {'model': LoginWithCredentialResponse, 'description': 'Logged in successfully'},
        403: {'model': LoginErrorResponse, 'description': 'Credential mismatch or account disabled.'}
    }
)
async def login_with_credential(cred: LoginWithCredentialForm, response: Response):
    auth = Auth()

    user = await db.find_one(Admin, (Admin.username == cred.username) | (Admin.email == cred.username) | (
                Admin.phone == cred.username))
    if user is None:
        user = await db.find_one(Client, (Client.username == cred.username) | (Client.email == cred.username) | (
                    Client.phone == cred.username))

    if user is not None:
        if auth.verify_password(cred.password, user.password):
            if user.status:
                access_token = auth.encode_token(user)
                refresh_token = auth.encode_refresh_token(user)
                return LoginWithCredentialResponse(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            else:
                response.status_code = status.HTTP_403_FORBIDDEN
                return LoginErrorResponse(
                    loc=['auth', 'login', 'credential'],
                    msg='Your account is disabled, Please contact administrator.'
                )

    response.status_code = status.HTTP_403_FORBIDDEN
    return LoginErrorResponse(
        loc=['auth', 'login', 'credential'],
        msg='Invalid credential provided, Please try with correct one.'
    )


@api.post(
    '/request-phone-login-otp',
    description='Request OTP for phone login.',
    responses={
        200: {'model': RequestOtpForPhoneLoginResponse, 'description': 'OTP sent to phone'},
        403: {'model': LoginErrorResponse, 'description': 'Phone number not found or account disabled.'}
    },
)
async def request_otp_for_phone_login(cred: RequestOtpForPhoneLoginForm, response: Response):
    user = await db.find_one(Admin, Admin.phone == cred.phone)
    if user is None:
        user = await db.find_one(Client, Client.phone == cred.phone)

    if user is not None:
        if user.status is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return LoginErrorResponse(
                loc=['auth', 'login', 'phone'],
                msg='Your account is disabled, Please contact administrator.'
            )

        if user.phone_login is None:
            #otp = random.randint(0000, 9999)
            otp = 1234
            message = f'Your MONDOLINT login otp is {otp}'
            report = SMS(to=user.phone, msg=message).send()
            phone_login = PhoneLogin(
                code=otp,
                expiry=datetime.utcnow() + timedelta(minutes=2)
            )

            user.phone_login = phone_login
            await db.save(user)

            return RequestOtpForPhoneLoginResponse(
                loc=['auth', 'login', 'phone', 'otp'],
                msg='OTP sent to your phone number.'
            )

        else:
            phone_login = user.phone_login
            updated_phone_login = PhoneLogin(
                code=phone_login.code,
                expiry=datetime.utcnow() + timedelta(minutes=2)
            )

            user.phone_login = updated_phone_login
            await db.save(user)

            return RequestOtpForPhoneLoginResponse(
                loc=['auth', 'login', 'phone', 'otp'],
                msg='OTP already sent to your phone.'
            )

    response.status_code = status.HTTP_403_FORBIDDEN
    return LoginErrorResponse(
        loc=['auth', 'login', 'phone'],
        msg='No user found with that phone number.'
    )


@api.post(
    '/login-with-phone',
    description='Login with phone.',
    responses={
        200: {'model': LoginWithPhoneResponse, 'description': 'Logged in successfully.'},
        403: {'model': LoginErrorResponse, 'description': 'Phone number not found or account disabled.'}
    }
)
async def login_with_phone(cred: LoginWithPhoneForm, response: Response):
    auth = Auth()
    user = await db.find_one(Admin, Admin.phone == cred.phone)
    if user is None:
        user = await db.find_one(Client, Client.phone == cred.phone)

    if user is not None:
        if user.status is False:
            response.status_code = status.HTTP_403_FORBIDDEN
            return LoginErrorResponse(
                loc=['auth', 'login', 'phone'],
                msg='Your account is disabled, Please contact administrator.'
            )

        if user.phone_login is None:
            return RequestOtpForPhoneLoginResponse(
                loc=['auth', 'login', 'phone', 'otp'],
                msg='You didn\'t even requested for a otp, Try to request OTP first.'
            )
        else:
            if user.phone_login.code == cred.code:
                user.phone_login = None
                await db.save(user)

                access_token = auth.encode_token(user)
                refresh_token = auth.encode_refresh_token(user)
                return LoginWithCredentialResponse(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            else:
                response.status_code = status.HTTP_403_FORBIDDEN
                return LoginErrorResponse(
                    loc=['auth', 'login', 'phone'],
                    msg='Invalid OTP provided, Please try with correct one.'
                )

    response.status_code = status.HTTP_403_FORBIDDEN
    return LoginErrorResponse(
        loc=['auth', 'login', 'phone'],
        msg='No user found with that phone number.'
    )


@api.post(
    '/request-reset-password-otp',
    description='Request password reset key.',
    responses={
        200: {'model': RequestResetPasswordOtpResponse},
        403: {'model': ResetPasswordErrorResponse}
    }
)
async def request_reset_password_otp(cred: RequestResetPasswordOtpForm, response: Response):
    user = None
    if cred.method == 'email':
        user = await db.find_one(Admin, Admin.email == cred.identity)
        if user is None:
            user = await db.find_one(Client, Client.email == cred.identity)

    elif cred.method == 'phone':
        user = await db.find_one(Admin, Admin.phone == cred.identity)
        if user is None:
            user = await db.find_one(Client, Client.phone == cred.identity)

    if user is not None:
        if 'reset_password' in user:
            if user.reset_password.sent:
                return RequestResetPasswordOtpResponse(
                    loc=['request', 'reset', 'password', 'otp'],
                    msg='Otp already sent to your {cred.method}'
                )
            else:
                # Have to send otp again here
                return RequestResetPasswordOtpResponse(
                    loc=['request', 'reset', 'password', 'otp'],
                    msg='Otp sent to your {cred.method}'
                )
        else:
            user.reset_password = ResetPassword(
                code='123456',
                expiry=datetime.utcnow() + timedelta(minutes=10),
                send_otp_to=cred.method
            )
            await db.save(user)

            return RequestResetPasswordOtpResponse(
                loc=['request', 'reset', 'password', 'otp'],
                msg='Otp sent to your {cred.method}'
            )

    response.status_code = status.HTTP_403_FORBIDDEN
    return ResetPasswordErrorResponse(
        loc=['request', 'reset', 'password', 'otp'],
        msg='No user found with the provided {cred.method}.'
    )


@api.post(
    '/verify-reset-password-otp',
    description='Verify password reset key.',
    responses={
        200: {'model': VerifyResetPasswordOtpResponse},
        403: {'model': ResetPasswordErrorResponse}
    }
)
async def verify_reset_password_otp(cred: VerifyResetPasswordOtpForm, response: Response):
    user = await db.find_one(Admin, (Admin.email == cred.identity) | (Admin.phone == cred.identity))
    if user is None:
        user = await db.find_one(Client, (Client.email == cred.identity) | (Client.phone == cred.identity))

    if user is not None:
        if user.reset_password is not None:
            if user.reset_password.verified:
                return VerifyResetPasswordOtpResponse(
                    loc=['request', 'reset', 'password', 'otp'],
                    msg='OTP verified already.'
                )
            else:
                if user.reset_password.code == cred.code:
                    user.reset_password.verified = True
                    await db.save(user)

                    return VerifyResetPasswordOtpResponse(
                        loc=['request', 'reset', 'password', 'otp'],
                        msg='OTP verified, You can proceed to reset your password.'
                    )
                else:
                    response.status_code = status.HTTP_403_FORBIDDEN
                    return ResetPasswordErrorResponse(
                        loc=['verify', 'reset', 'password', 'otp'],
                        msg='Invalid OTP provided, Try with correct one.'
                    )
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return ResetPasswordErrorResponse(
                loc=['verify', 'reset', 'password', 'otp'],
                msg='Didn\'t even requested for the OTP, Try to do that first.'
            )

    response.status_code = status.HTTP_403_FORBIDDEN
    return VerifyResetPasswordOtpResponse(
        loc=['verify', 'reset', 'password', 'otp'],
        msg='User not found with the identity provided.'
    )


@api.post(
    '/reset-password',
    description='',
    responses={
        200: {'model': ResetPasswordResponse},
        403: {'model': ResetPasswordErrorResponse}
    }
)
async def reset_password(cred: ResetPasswordForm, response: Response):
    auth = Auth()
    user = await db.find_one(Admin, (Admin.email == cred.identity) | (Admin.phone == cred.identity))
    if user is None:
        user = await db.find_one(Client, (Client.email == cred.identity) | (Client.phone == cred.identity))

    if user is not None:
        if user.reset_password.verified:
            if cred.password == cred.confirm_password:
                user.password = auth.encode_password(cred.password)
                await db.save(user)

                return ResetPasswordResponse(
                    loc=['reset', 'password', 'otp'],
                    msg='Password reset successfully, You can now proceed to login.'
                )
            else:
                response.status_code = status.HTTP_403_FORBIDDEN
                return ResetPasswordErrorResponse(
                    loc=['reset', 'password', 'otp'],
                    msg='Password doesn\'t match the confirm password field.'
                )
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return ResetPasswordErrorResponse(
                loc=['reset', 'password', 'otp'],
                msg='OTP is not verified.'
            )

    response.status_code = status.HTTP_403_FORBIDDEN
    return ResetPasswordErrorResponse(
        loc=['reset', 'password', 'otp'],
        msg='No user found with the provided identity.'
    )


@api.post(
    '/refresh-token',
    description='Update access token by refresh token.',
    responses={
        200: {'model': LoginWithCredentialResponse, 'description': 'Logged in successfully'},
        403: {'model': LoginErrorResponse, 'description': 'Credential mismatch or account disabled.'}
    }
)
async def login_with_credential(cred: RefreshTokenForm, response: Response):
    auth = Auth()
    rt = auth.decode_refresh_token(cred.refresh_token)

    if rt['user']['type'] == 'admin':
        user = await db.find_one(Admin, Admin.id == ObjectId(rt['user']['id']))
    else:
        user = await db.find_one(Client, Client.id == ObjectId(rt['user']['id']))

    if user is not None:
        if user.status:
            access_token = auth.encode_token(user)
            if datetime.strptime(rt['expiry'], '%Y-%m-%d %H:%M:%S.%f') <= datetime.utcnow() + timedelta(days=10):
                refresh_token = auth.encode_refresh_token(user)
                return LoginWithCredentialResponse(
                    access_token=access_token,
                    refresh_token=refresh_token
                )
            else:
                return LoginWithCredentialResponse(
                    access_token=access_token,
                    refresh_token=cred.refresh_token
                )
        else:
            response.status_code = status.HTTP_403_FORBIDDEN
            return LoginErrorResponse(
                loc=['auth', 'login', 'credential'],
                msg='Your account is disabled, Please contact administrator.'
            )

    response.status_code = status.HTTP_403_FORBIDDEN
    return LoginErrorResponse(
        loc=['auth', 'login', 'credential'],
        msg='Invalid Refresh Token provided, Please try with correct one.'
    )


@api.get(
    '/get-user-detail',
    description='Get Logged in user details.',
    responses={
        200: {'model': LoggedInUserResponse, 'description': 'Logged in successfully'},
        403: {'model': LoginErrorResponse, 'description': 'Credential mismatch or account disabled.'}
    }
)
async def get_logged_in_user_detail(response: Response, token=Depends(Auth().wrapper)):
    role = None
    if token['user']['type'] == 'admin':
        user = await db.find_one(Admin, Admin.id == ObjectId(token['user']['id']))
        role = await db.find_one(Role, Role.id == ObjectId(token['user']['role']))
    else:
        user = await db.find_one(Client, Client.id == ObjectId(token['user']['id']))

    if user is not None:
        return LoggedInUserResponse(
            user=user,
            role=role
        )

    response.status_code = status.HTTP_403_FORBIDDEN
    return LoginErrorResponse(
        loc=['auth', 'login', 'credential'],
        msg='Invalid Refresh Token provided, Please try with correct one.'
    )
