from odmantic import EmbeddedModel, Field
from typing import Optional
from enum import Enum


# Import Utils
from datetime import datetime


class PhoneLogin(EmbeddedModel):
    code: str
    expiry: datetime
    sent: bool = Field(default=False)
    sent_at: Optional[datetime]


class SendCodeTo(str, Enum):
    EMAIL = "email"
    PHONE = "phone"


class ResetPassword(EmbeddedModel):
    code: str
    expiry: datetime
    sent: bool = Field(default=False)
    sent_at: Optional[datetime]
    send_otp_to: SendCodeTo
    verified: bool = Field(default=False)
