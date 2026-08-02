from bs4 import BeautifulSoup
import json
import csv
from pprint import pprint
import requests

def parse_product(product, counter):
    data = dict()
    data["local_id"] = counter
    data["online_id"] = product.get("productID", None)
    data["name"] = product.get("name", None)
    data["sku"] = product.get("sku", None)
    data["isbn"] = product.get("isbn", None)
    data["image"] = product.get("image", None)
    data["description"] = product.get("description", None)
    data["url"] = product.get("offers", {}).get("url")
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
FIELD_NAMES = ["local_id", "online_id", "name", "sku", "isbn", "image", "description", "url", "price"]
with open("data/all_products_db.csv", "a", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
    if csv_file.tell() == 0:
        writer.writeheader()

    for link in individual_product_links:
        try:
            individual_page = requests.get(link, headers=user_agent, timeout=60)
        except Exception as e:
            print(f"Page fetch failed: {e}")
            continue

        try:
            content = BeautifulSoup(individual_page.text, "html.parser")
            data = content.find_all("script", {"type" : "application/ld+json"})[1]
            json_data = json.loads(data.string)

            formatted = parse_product(json_data, counter)
            all_products.append(formatted)

            counter += 1
        except Exception as e:
            print(f"Failed parsing: {e}")
            continue

        try:
            writer.writerow(formatted)
            csv_file.flush()
            print("Written to CSV", counter)
        except Exception as e:
            print(f"Couldn't write to csv {e}")

        if counter % 50 == 0:
            try:
                with open("products_db.json", "w", encoding="utf-8") as file:
                    json.dump(all_products, file, indent=4)
                print("WRITTEN TO JSON FILE")
            except Exception as e:
                print(f"Failed writing to file: {e}")
