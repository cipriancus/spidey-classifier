from currency_converter import CurrencyConverter

currency_converter = CurrencyConverter()


def strip_from_currency(amount):
    str_curr = ''
    for iterator in amount:
        if not iterator.isdigit() and iterator != '.' and iterator != ',':
            str_curr = str_curr + iterator
    if str_curr == 'US $' or str_curr == '$':
        str_curr = "USD"
    if str_curr == 'C':
        str_curr = "CAD"
    if '£' in str_curr:
        str_curr = 'GBP'
    return str_curr.replace(' ', '')


def strip_amount(amount, currency):
    currency_separators = ['.', ',']
    amount.replace(currency, '')
    new_amount = ''
    for iterator in amount:
        if iterator.isdigit() or iterator in currency_separators:
            new_amount = new_amount + iterator
    return new_amount.replace(',', '.')


def convert_currency(price, to_currency='EUR'):
    from_currency = strip_from_currency(price)
    amount = strip_amount(price, from_currency)
    return currency_converter.convert(float(amount), from_currency, to_currency)
