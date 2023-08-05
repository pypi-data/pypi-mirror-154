import decimal
from decimal import localcontext
from typing import Union

from .types import is_integer, is_string
from .units import units


class denoms:
    von = int(units["von"])
    kvon = int(units["kvon"])
    kvon = int(units["kvon"])
    kvon = int(units["kvon"])
    mvon = int(units["mvon"])
    mvon = int(units["mvon"])
    mvon = int(units["mvon"])
    gvon = int(units["gvon"])
    gvon = int(units["gvon"])
    gvon = int(units["gvon"])
    gvon = int(units["gvon"])
    microlat = int(units["microlat"])
    microlat = int(units["microlat"])
    microlat = int(units["microlat"])
    millilat = int(units["millilat"])
    millilat = int(units["millilat"])
    millilat = int(units["millilat"])
    lat = int(units["lat"])
    klat = int(units["klat"])
    klat = int(units["klat"])
    mlat = int(units["mlat"])
    glat = int(units["glat"])
    tlat = int(units["tlat"])


MIN_VON = 0
MAX_VON = 2 ** 256 - 1


def from_von(number: int, unit: str) -> Union[int, decimal.Decimal]:
    """
    Takes a number of von and converts it to any other lat unit.
    """
    if unit.lower() not in units:
        raise ValueError(
            "Unknown unit.  Must be one of {0}".format("/".join(units.keys()))
        )

    if number == 0:
        return 0

    if number < MIN_VON or number > MAX_VON:
        raise ValueError("value must be between 1 and 2**256 - 1")

    unit_value = units[unit.lower()]

    with localcontext() as ctx:
        ctx.prec = 999
        d_number = decimal.Decimal(value=number, context=ctx)
        result_value = d_number / unit_value

    return result_value


def to_von(number: Union[int, float, str, decimal.Decimal], unit: str) -> int:
    """
    Takes a number of a unit and converts it to von.
    """
    if unit.lower() not in units:
        raise ValueError(
            "Unknown unit.  Must be one of {0}".format("/".join(units.keys()))
        )

    if is_integer(number) or is_string(number):
        d_number = decimal.Decimal(value=number)
    elif isinstance(number, float):
        d_number = decimal.Decimal(value=str(number))
    elif isinstance(number, decimal.Decimal):
        d_number = number
    else:
        raise TypeError("Unsupported type.  Must be one of integer, float, or string")

    s_number = str(number)
    unit_value = units[unit.lower()]

    if d_number == decimal.Decimal(0):
        return 0

    if d_number < 1 and "." in s_number:
        with localcontext() as ctx:
            multiplier = len(s_number) - s_number.index(".") - 1
            ctx.prec = multiplier
            d_number = decimal.Decimal(value=number, context=ctx) * 10 ** multiplier
        unit_value /= 10 ** multiplier

    with localcontext() as ctx:
        ctx.prec = 999
        result_value = decimal.Decimal(value=d_number, context=ctx) * unit_value

    if result_value < MIN_VON or result_value > MAX_VON:
        raise ValueError("Resulting von value must be between 1 and 2**256 - 1")

    return int(result_value)
