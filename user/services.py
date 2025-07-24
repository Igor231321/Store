import re

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


def normalize_phone_number(string):
    cleaned = re.sub(r"[^\d+]", "", string)

    try:
        phone_number = phonenumbers.parse(cleaned, "UA")
        if not phonenumbers.is_valid_number(phone_number):
            return None
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return None
