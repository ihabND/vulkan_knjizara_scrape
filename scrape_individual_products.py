from bs4 import BeautifulSoup
import json
import csv
import os
from pprint import pprint
import requests

CHUNK_SIZE = 1000

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

def dump_chunk(products, start_id):
    end_id = start_id + len(products) - 1
    path = f"data/json_db/products_db_{start_id}_{end_id}.json"
    try:
        os.makedirs("data/json_db", exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(products, file, indent=4, ensure_ascii=False)
        print(f"WRITTEN TO JSON FILE: {path} ({len(products)} products)")
        return True
    except Exception as e:
        print(f"Failed writing to file: {e}")
        return False

with open("data/ALL_LINKS.txt", "r", encoding="utf-8") as file:
    individual_product_links = file.readlines()
individual_product_links = [link.strip() for link in individual_product_links]

user_agent = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    )
}

FIELD_NAMES = ["local_id", "online_id", "name", "sku", "isbn", "image", "description", "url", "price"]

counter = 1
done_links = set()
if os.path.exists("data/all_products_db.csv"):
    with open("data/all_products_db.csv", "r", newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            done_links.add(row["url"])
            try:
                counter = max(counter, int(row["local_id"]) + 1)
            except (TypeError, ValueError):
                continue
if done_links:
    print(f"Resuming at local_id {counter}, skipping {len(done_links)} already scraped links")

all_products = []
chunk_start = counter
with open("data/all_products_db.csv", "a", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
    if csv_file.tell() == 0:
        writer.writeheader()

    for link in individual_product_links:
        if link in done_links:
            continue

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
            print("Written to CSV", formatted["local_id"])
        except Exception as e:
            print(f"Couldn't write to csv {e}")
            all_products.pop()
            counter -= 1
            continue

        if len(all_products) == CHUNK_SIZE:
            if dump_chunk(all_products, chunk_start):
                chunk_start = counter
                all_products = []

if all_products:
    dump_chunk(all_products, chunk_start)
