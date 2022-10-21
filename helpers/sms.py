from fastapi import HTTPException, status
from settings import settings

# Import Utils
import requests
import phonenumbers


class SMS:

    def __init__(self, msg=None, to=None, request_id=None):
        self.host = settings.SMS_API_HOST
        self.sms_path = settings.SMS_API_SENDING_PATH
        self.report_path = settings.SMS_API_REPORT_PATH
        self.key = settings.SMS_API_KEY
        self.request_id = request_id
        self.msg = msg
        self.to = to

    def message(self, msg):
        self.msg = msg

    def recipient(self, number):
        self.to = number

    def request(self, req_id):
        self.request_id = req_id

    def send(self):
        try:
            number = phonenumbers.parse(self.to)
            if number.country_code == 880:
                payload = {
                    'api_key': self.key,
                    'msg': self.msg,
                    'to': self.to
                }
                response = requests.request('POST', f'{self.host}{self.sms_path}', data=payload)
                return response
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=dict(
                        loc=['sms'],
                        msg='Can not sent login otp in this number.',
                        type='value_error.number.country.not.supported'
                    )
                )
        except():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=dict(
                    loc=['sms'],
                    msg='Invalid phone number provided.',
                    type='value_error.invalid.number'
                )
            )

    def report(self):
        response = requests.request('GET', f'{self.host}{self.report_path}{self.request_id}')
        return response.json()
