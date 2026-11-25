"""Money helpers. All amounts are integer minor units (cents)."""

_SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£"}
_ZERO_DECIMAL = {"JPY"}


def round_half_even(numerator, denominator):
    """Integer division rounding half to even (banker's rounding)."""
    q, r = divmod(numerator, denominator)
    twice = 2 * r
    if twice > denominator or (twice == denominator and q % 2 == 1):
        q += 1
    return q


def format_money(cents, currency="USD"):
    """Format integer cents, e.g. format_money(123456, 'USD') -> '$1,234.56'."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    if currency in _ZERO_DECIMAL:
        return f"{sign}¥{cents:,}"
    symbol = _SYMBOLS.get(currency, currency + " ")
    return f"{sign}{symbol}{cents // 100:,}.{cents % 100:02d}"
