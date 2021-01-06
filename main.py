import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

BITCOIN_URL = 'https://api.blockchain.com/v3/exchange/tickers/BTC-USD'
ETHERENUM_URL = 'https://api.blockchain.com/v3/exchange/tickers/ETH-USD'
EXCHANGE_URL = 'https://free.currconv.com/api/v7/convert?q=USD_PLN&compact=ultra&apiKey=[api_key]'
WEBHOOK_URL = ''


def get_pasztetowa_price():
    r = requests.get(
        "https://www.carrefour.pl/artykuly-spozywcze/konserwy-i-dania-gotowe/pasztety?")
    soup = BeautifulSoup(r.text, 'html.parser')

    price = soup.select_one(
        ".MuiTypography-root.MuiTypography-caption.MuiTypography-colorTextSecondary:nth-child(2)").text
    price = eval(price.replace(
        " zł/1 kg", "").replace(",", "."))

    return price


def get_kozaki_price():
    r = requests.get(
        "https://www.eobuwie.com.pl/meskie/kozaki-i-inne/kozaki.html?test_f=2")
    soup = BeautifulSoup(r.text, 'html.parser')

    price = soup.select_one(
        ".products-list__regular-price").text
    for i in {'\n', u'\xa0', "zł "}:
        price = price.replace(i, "")
    price = eval(price.replace(",", "."))

    return price


def get_uno_price():
    r = requests.get(
        "https://www.olx.pl/oferty/q-fiat-uno/?search%5Border%5D=filter_float_price%3Adesc&search%5Bfilter_float_price%3Ato%5D=10000")
    soup = BeautifulSoup(r.text, 'html.parser')

    price = soup.select_one(".space.inlblk.rel strong").text
    price = eval(price.replace(
        " zł", "").replace(",", ".").replace(" ", ""))

    return price


pasztetowa_price = get_pasztetowa_price()
kozaki_price = get_kozaki_price()
uno_price = get_uno_price()

btc_price = requests.get(BITCOIN_URL).json().get("price_24h")
eth_price = requests.get(ETHERENUM_URL).json().get("price_24h")
usd2pln_price = requests.get(EXCHANGE_URL).json().get("USD_PLN")

btc2pln = btc_price * usd2pln_price
eth2pln = eth_price * usd2pln_price

btc_kozaki_count = btc2pln / kozaki_price
btc_pasztetowa_count = btc2pln / pasztetowa_price
btc_uno_count = btc2pln / uno_price
eth_kozaki_count = eth2pln / kozaki_price
eth_pasztetowa_count = eth2pln / pasztetowa_price
eth_uno_count = eth2pln / uno_price

date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

msg = f"""```md
# Dzień dobry! dziś mamy {date}

Bitcoin kosztuje {btc2pln:08,.2f} PLN tj.

[1]: {btc_kozaki_count:01,.1f} par kozaków
[2]: {btc_pasztetowa_count:01,.1f} kg pasztetowej
[3]: {btc_uno_count:01,.1f} fiatów uno


Etherenum kosztuje {eth2pln:01,.1f} PLN tj.

[1]: {eth_kozaki_count:01,.1f} par kozaków
[2]: {eth_pasztetowa_count:01,.1f} kg pasztetowej
[3]: {eth_uno_count:01,.1f} fiatów uno
```"""

r = requests.post(WEBHOOK_URL, json={"content": msg})
