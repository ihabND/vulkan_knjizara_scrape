from bs4 import BeautifulSoup
import json
from pprint import pprint
import requests

def parse_product(product, counter):
    data = dict()
    data["id"] = counter
    data["name"] = product.get("name", None)
    data["sku"] = product.get("sku", None)
    data["isbn"] = product.get("isbn", None)
    data["price"] = product.get("offers", {}).get("price")
    return data

with open("data/ALL_LINKS.txt", "r", encoding="utf-8") as file:
    individual_product_links = file.readlines()
individual_product_links = [link.strip() for link in individual_product_links]

user_agent = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
}

counter = 1
all_products = []
for link in individual_product_links:
    try:
        individual_page = requests.get(link, headers=user_agent, timeout=60)
    except Exception as e:
        print(f"Page fetch failed: {e}")
        continue

    content = BeautifulSoup(individual_page.text, "html.parser")
    data = content.find_all("script", {"type" : "application/ld+json"})[1]
    json_data = json.loads(data.string)

    formatted = parse_product(json_data, counter)
    all_products.append(formatted)

    print("SCRAPING...", counter)
    counter += 1

    with open("products_db.json", "w", encoding="utf-8") as file:
        json.dump(all_products, file, indent=4)

