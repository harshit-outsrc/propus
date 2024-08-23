import functools
import json
import re
import string
import secrets
from typing import Union, AnyStr, Dict

from propus.helpers.exceptions import JSONDecodeError
from propus.helpers.city_to_county import city_to_county_map
from propus.helpers.zip_to_county import zip_to_county_map


TRUE_VALUES = (
    True,
    1,
    "1",
    "true",
    "t",
    "yes",
    "y",
)

FALSE_VALUES = (
    False,
    0,
    "0",
    "false",
    "f",
    "no",
    "n",
)

NULL_VALUES = (
    None,
    "",
    "none",
    "null",
)


def is_none(func):
    """
    Wrapper function to tell if single argument passed to func should
    return None,or if the function should proceed with additional checks.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args or args[0] is None or str(args[0]).lower() in NULL_VALUES:
            return None
        return func(*args, **kwargs)

    return wrapper


def get_bool(value):
    try:
        if value in NULL_VALUES:
            raise ValueError
        elif value in TRUE_VALUES:
            return True
        elif value in FALSE_VALUES:
            return False
        elif value.lower() in TRUE_VALUES:
            return True
        elif value.lower() in FALSE_VALUES:
            return False
        else:
            raise ValueError

    except Exception as e:
        raise ValueError(f"Error converting to bool ({value}): {e}")


@is_none
def get_bool_or_none(value):
    try:
        return get_bool(value)
    except Exception as e:
        raise ValueError(f"Error converting to bool ({value}): {e}")


def get_int(value):
    try:
        return int(value)
    except Exception as e:
        raise ValueError(f"Error converting to int ({value}): {e}")


@is_none
def get_int_or_none(value):
    try:
        return get_int(value)
    except Exception as e:
        raise ValueError(f"Error converting to int ({value}): {e}")


def get_string(value):
    try:
        return str(value)
    except Exception as e:
        raise TypeError(f"Error converting to string ({value}): {e}")


@is_none
def get_string_or_none(value=None):
    try:
        return get_string(value)
    except Exception as e:
        raise TypeError(f"Error converting to string ({value}): {e}")


def clean_phone(value):
    if isinstance(value, int):
        value_string = str(value)
    elif isinstance(value, str):
        value_string = re.sub("[^0-9]", "", value)
    else:
        raise ValueError(f"Phone number ({value}) is not a parseable string or integer.")

    if len(value_string) == 10:
        return value_string
    elif len(value_string) == 11 and value_string[0:1] == "1":
        return value_string[1:]
    else:
        raise ValueError(f"Phone number ({value}) should contain ten digits.")


def clean_null_bytes(value: Union[str, bytes]):
    if isinstance(value, str):
        return value.replace("\x00", "")
    elif isinstance(value, bytes):
        return value.replace(b"\x00", b"")

    raise ValueError(f"Passed ({value}) is not a String or Bytes type.")


def clean_ssn(value):
    if isinstance(value, int):
        value_string = str(value)
    elif isinstance(value, str):
        value_string = re.sub("[^0-9X]", "", value)
    else:
        raise ValueError(f"SSN ({value}) is not a parseable string or integer.")

    # Clean dummy values entered in, e.g., 000000000
    if len(value_string) == 9:
        for i in range(0, 10):
            if value_string == f"{i}{i}{i}{i}{i}{i}{i}{i}{i}":
                value_string = None
                break
        return value_string
    # Pad with placeholder values if only the last four digits have been provided
    elif len(value_string) == 4:
        return f"XXXXX{value_string}"
    else:
        raise ValueError(f"SSN ({value}) should contain nine digits or X.")


def decode_json(data: AnyStr) -> Dict:
    """
    Decode JSON String

    Args:
        data (str): jsonified string to be decoded

    Raises:
        InvalidAPIUsage: if the data sent is an invalid JSON object an error response will be returned

    Returns:
        Dict: returns the json loaded dictionary
    """
    try:
        return json.loads(data)
    except Exception:
        raise JSONDecodeError(data)


def batch_generator(input_list, batch_size):
    """
    Generates batches of a specified size from a list.

    Args:
    input_list (list): The original list.
    batch_size (int): The size of each batch.

    Yields:
    list: A batch of up to batch_size elements.
    """
    for i in range(0, len(input_list), batch_size):
        yield input_list[i : i + batch_size]  # noqa: E203


def generate_password(length=16):
    """Generates password based on upper and lower case alphabetical characters and digits.

    Args:
        length (int, optional): Length of the password to generate. Defaults to 16.

    Returns:
        str: string of the password generated
    """
    password_characters = string.ascii_letters + string.digits
    password = "".join(secrets.choice(password_characters) for i in range(length))
    return password


def fetch_county(city: AnyStr = None, zip_code: AnyStr = None) -> AnyStr:
    """
    Fetches county from city or zip code.

    Args:
        city (AnyStr, optional): City name. Defaults to None.
        zip_code (AnyStr, optional): Zip code. Defaults to None.

    Returns:
        AnyStr: County name. Returns None if no match found.
    """
    if not city and not zip_code:
        return None
    if city:
        city = city.lower().replace(" ", "")
    return (
        zip_to_county_map.get(zip_code)
        if zip_code and zip_to_county_map.get(zip_code)
        else city_to_county_map.get(city)
    )
