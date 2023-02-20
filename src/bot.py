import requests
import argparse
from bs4 import BeautifulSoup

_title_class = "app-header__title"
_price_class = "app-header__list__item--price"
_rating_class = "we-customer-ratings__averages__display"
_count_class = "we-customer-ratings__count"
_icon_class = "we-artwork--ios-app-icon"

class App():

    def __init__(self):
        self.id = "id"
        self.name = "name"
        self.price = "price"
        self.rating = "rating"
        self.rating_amount = "amount"
        self.icon = "icon"

    def __str__(self):
        return f"{self.name} - R${self.price} ({self.rating} of 5,0 stars - {self.rating_amount} votes)"

    def to_sql(self):
        return f"('{self.id}', '{self.name}', {self.price}, {self.rating}, '{self.rating_amount}', '{self.icon}')"

def make_url(id,locale="br"):
    return f"https://apps.apple.com/{locale}/app/id{id}"

def get_page(id):
    r = requests.get(make_url(id))
    if(r.status_code == 200):
        return r.text
    return False

def create_model(html, id):
    try:
        soup = BeautifulSoup(html, "html.parser")
    except TypeError:
        print("App não encontrado")
        return False

    new_app = App()
    try:
        new_app.id = id
        #Get app's name
        name = soup.find_all("h1", _title_class)[0]
        new_app.name = name.find(string=True,recursive=False).strip()

        #Get app's price
        price = soup.find_all("li", _price_class)[0]
        parsed_price = price.string.strip("R$").strip()
        if parsed_price == "Grátis":
            new_app.price = float(0)
        else:
            new_app.price = float(parsed_price.replace(",","."))
        try:
            #Get app's rating
            rating = soup.find_all("span", _rating_class)[0]
            new_app.rating = float(rating.string.strip().replace(",","."))

            #Get app's amount of counts
            count = soup.find_all("div", _count_class)[0]
            new_app.rating_amount = count.string.strip("avaliações").strip()

        except IndexError:
            new_app.rating = float(0)
            new_app.rating_amount = "0"

        #Get app's icon
        icon = soup.find_all("picture", _icon_class)[0]
        icon = icon.find("source")
        new_app.icon = icon["srcset"].split()[0]
        return new_app
    except: #generic one
        return False

def fetch(id):
    html = get_page(id)
    return create_model(html, id)

if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("id")
    parsed = arg.parse_args()

    b = fetch(parsed.id)
    print(b)
