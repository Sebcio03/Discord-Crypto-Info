import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

BITCOIN_URL = 'https://api.blockchain.com/v3/exchange/tickers/BTC-USD'
# Free exchange api ;)
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

    price = soup.select_one(
        ".space.inlblk.rel strong").text
    price = eval(price.replace(
        " zł", "").replace(",", ".").replace(" ", ""))

    return price


bitcoin_price = requests.get(BITCOIN_URL).json().get("price_24h")
if not bitcoin_price:
    exit()

usd2pln_price = requests.get(EXCHANGE_URL).json().get("USD_PLN")
if not usd2pln_price:
    exit()

bitcoin2pln = bitcoin_price * usd2pln_price
date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
kozaki_count = bitcoin2pln // get_kozaki_price()
pasztetowa_count = bitcoin2pln // get_pasztetowa_price()
uno_count = bitcoin2pln // get_uno_price()

msg = f"""```md
# Dzień dobry! dziś mamy {date}
Bitcoin kosztuje <{round(bitcoin2pln,0)}PLN> tj.

[1]: {kozaki_count} par kozaków
[2]: {pasztetowa_count} kg pasztetowej
[3]: {uno_count} fiatów uno
```"""

r = requests.post(WEBHOOK_URL, json={"content": msg})
