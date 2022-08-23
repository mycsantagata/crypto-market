import requests


class CMC:

    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion"

        self.params = {
            'amount': '1',
            'symbol': 'BTC',
            'convert': 'USD'
        }

        self.headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "fe8ce252-6efe-4dbb-8c94-3bba3908e353"
        }

    def getBTCPrice(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']['quote']['USD']['price']

