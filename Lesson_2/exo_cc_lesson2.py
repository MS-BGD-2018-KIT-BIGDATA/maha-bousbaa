

import requests
from bs4 import BeautifulSoup

URL_ordinateur_acer = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-acer.html#_his_"
URL_ordinateur_dell = "https://www.cdiscount.com/informatique/ordinateurs-pc-portables/pc-portables/lf-228394_6-dell.html#_his_"

def get_promotions(url):
    rebates = []
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    prdt_blocs = soup.find_all("div", class_="prdtBloc")
    for product in prdt_blocs:
        prices = getPrices(product)
        rebates.append(prices[0] / prices[1])
    return rebates

def print_promotions(promos):
    print("ratio promotion:")
    for promo in promos:
        print(promo)

def getPrices(tag):
    current_str_price = tag.find_all("div", class_="prdtPrice")[0].find_all("span", class_ = "price")[0].contents[0]
    current_price = int(current_str_price)
    previous_str_price_tag = tag.find_all("div", class_="prdtPInfoT")[
        0].find_all("div", class_="prdtPrSt")
    if len(previous_str_price_tag) == 0:
        previous_price = current_price
    else:
        previous_price = int(previous_str_price_tag[0].string.split(",")[0])
    return previous_price, current_price

print("portable Dell")
print_promotions(get_promotions(URL_ordinateur_dell))

print("\n portable Acer")
print_promotions(get_promotions(URL_ordinateur_acer))

