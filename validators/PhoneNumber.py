import phonenumbers


class PhoneNumber(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            number = phonenumbers.parse(v, None)
            if phonenumbers.is_valid_number(number):
                return v
            else:
                raise ValueError("invalid.phone.number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError("invalid.phone.number")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
