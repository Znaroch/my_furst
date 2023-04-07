import requests
import json
from config import keys


class ConvertException(Exception):
    pass


class ConvertValues:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertException(f'Невозможно конвертировать одинаковые валюты {keys[quote]}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {keys[quote]}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту {keys[base]}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException('Не удалось обработать количество {amount)}')

        r = requests.get(
            f"https://api.currencyapi.com/v3/latest?apikey=zuapzhW2yQNyARlAU1aEo88rftSYHov2BtsmHIG0&currencies={base_ticker}&base_currency={quote_ticker}")

        text = json.loads(r.content)
        result = text['data']
        f = result[keys[base]]
        main_result = f['value']
        main = float(amount) * float(main_result)
        return main
