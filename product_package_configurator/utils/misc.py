from odoo.tools import float_round


def multiply(unit: float, multiplier: float, digits=None):
    val = unit * multiplier
    if digits is not None:
        val = float_round(val, precision_digits=digits)
    return val
