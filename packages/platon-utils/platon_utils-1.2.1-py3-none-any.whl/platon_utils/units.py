import decimal

# Units are in their own module here, so that they can keep this
# formatting, as this module is excluded from black in pyproject.toml
# fmt: off
units = {
    'von':          decimal.Decimal('1'),
    'kvon':         decimal.Decimal('1000'),
    'mvon':         decimal.Decimal('1000000'),
    'gvon':         decimal.Decimal('1000000000'),
    'microlat':     decimal.Decimal('1000000000000'),
    'millilat':     decimal.Decimal('1000000000000000'),
    'lat':          decimal.Decimal('1000000000000000000'),
    'klat':         decimal.Decimal('1000000000000000000000'),
    'mlat':         decimal.Decimal('1000000000000000000000000'),
    'glat':         decimal.Decimal('1000000000000000000000000000'),
    'tlat':         decimal.Decimal('1000000000000000000000000000000'),
}
# fmt: on
